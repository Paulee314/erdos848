// gen848.c — seating-chart (colouring) certificates for Erdős #848, all plateaus up to Nmax.
// Certificate for plateau k (N in [25k+7, 25k+31], c(N)=k+1): every candidate n <= N (n^2+1 not squarefree)
// is put in one of k+1 classes (one per anchor a_m = 25m+7, m <= k) so that uv+1 is squarefree for every
// pair u != v in a class. Output: global assignment + per-plateau re-homing of 18-mod-25 numbers.
// Usage: gen848 Nmax outdir      (Nmax is rounded down to 25K+31)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
typedef unsigned long long u64; typedef __uint128_t u128; typedef long long i64;

static u64 *sp; static int nsp;                 // small primes for squarefree test
static long long nsqtests=0;
static int is_sqfree(u64 n){                    // n <= ~1e18; trial division to cbrt(n) + square check
    nsqtests++;
    u64 r=n;
    for(int i=0;i<nsp;i++){ u64 p=sp[i]; if(p*p*p>n) break;
        if(r%p==0){ r/=p; if(r%p==0) return 0; } }
    u64 q=(u64)sqrtl((long double)r); while(q*q>r) q--; while((q+1)*(q+1)<=r) q++;
    return !(q>1 && q*q==r);
}
static u64 mulmod(u64 a,u64 b,u64 m){ return (u64)((u128)a*b%m); }
static u64 powmod(u64 a,u64 e,u64 m){ u64 r=1%m; a%=m; while(e){ if(e&1) r=mulmod(r,a,m); a=mulmod(a,a,m); e>>=1;} return r; }

// ---- classes ----
#define CAP 8
typedef struct { int n; u64 v[CAP]; } Cls;
static Cls *cls; static int K;
static u64 A(int m){ return 25ULL*m+7; } static u64 X(int j){ return 25ULL*j+18; }
static int *matchX,*matchA;                     // global x<->anchor matching
static const int SH[]={-1,-4,-5,-6,-8,-10,-12,2,3,4,6,8,10,11,12};
#define NSH (int)(sizeof(SH)/sizeof(SH[0]))
static signed char *edge;                       // edge[j*NSH+s]: -1 unknown, 0 no, 1 yes
static int has_edge(int j,int s){ int m=j+SH[s]; if(m<0||m>K) return 0; signed char *e=&edge[(size_t)j*NSH+s];
    if(*e<0) *e=is_sqfree(X(j)*A(m)+1); return *e; }
static int *vis; static int stamp=0;
static int kuhn(int j,int depth){               // augmenting path for x_j in the global matching
    if(depth>50) return 0;
    for(int s=0;s<NSH;s++){ int m=j+SH[s]; if(m<0||m>K||!has_edge(j,s)||vis[m]==stamp) continue; vis[m]=stamp;
        if(matchA[m]<0 || kuhn(matchA[m],depth+1)){ matchA[m]=j; matchX[j]=m; return 1; } }
    return 0;
}

// ---- per-plateau re-homing ----
// first conflict of x_j with the non-x members of class m (smallest member value w with x_j*w+1 not squarefree)
typedef struct { u64 key; u64 val; } HE; static HE *ht; static u64 hmask;
static u64 first_conflict(int j,int m){
    u64 key=((u64)j<<32)|(u64)m, h=((key*0x9E3779B97F4A7C15ULL)>>40) & hmask;
    if(ht[h].key==key+1) return ht[h].val;
    u64 best=~0ULL, x=X(j);
    for(int i=0;i<cls[m].n;i++){ u64 w=cls[m].v[i]; if(w%25==18) continue; if(w<best && !is_sqfree(x*w+1)) best=w; }
    ht[h].key=key+1; ht[h].val=best; return best;
}
// local matching at plateau k among candidate anchors; uses undo arrays
static int *lmA,*lmX,*lvis; static int lstamp=0; static int S_SWAP=60, T_TOP=40;
static int curk; static u64 curN; static int *freeA; static int nfreeA; static int *U; static int nU;
static int anchor_ok(int m){ return (m<S_SWAP && m<=curk) || (m>=curk-T_TOP && m<=curk) || (matchA[m]<0) || (matchA[m]>curk); }
static int *touchedA,*touchedX; static int ntA,ntX;
static int gA(int m){ return lmA[m]; } static int gX(int j){ return lmX[j]; }
static void sA(int m,int j){ touchedA[ntA++]=m; lmA[m]=j; } static void sX(int j,int m){ touchedX[ntX++]=j; lmX[j]=m; }
static int *parX,*bq;
static int lbfs(int root){
    lstamp++; int qh=0,qt=0; bq[qt++]=root;
    static const int ORD[3]={2,1,0};
    while(qh<qt){ int u=bq[qh++];
        int lists[2][2]={{0,S_SWAP-1},{curk-T_TOP,curk}};
        for(int LL=0;LL<3;LL++){ int L=ORD[LL]; int lo,hi; if(L<2){ lo=lists[L][0]<0?0:lists[L][0]; hi=lists[L][1]>curk?curk:lists[L][1]; } else { lo=0; hi=nfreeA-1; }
            for(int it=lo;it<=hi;it++){ int m=(L<2)?it:freeA[it]; if(m>curk) break; if(lvis[m]==lstamp) continue;
                if(first_conflict(u,m)<=curN) continue;
                lvis[m]=lstamp; parX[m]=u;
                if(gA(m)<0){
                    int cm=m;
                    for(;;){ int w=parX[cm]; int prev=gX(w); sA(cm,w); sX(w,cm); if(w==root||prev<0) break; cm=prev; }
                    return 1; }
                bq[qt++]=gA(m); } } }
    return 0;
}
int main(int argc,char**argv){
    if(argc<3){ fprintf(stderr,"usage: gen848 Nmax outdir\n"); return 1; }
    u64 Nmax=strtoull(argv[1],0,10); K=(int)((Nmax-31)/25); Nmax=25ULL*K+31;
    const char*od=argv[2];
    // primes up to Nmax
    unsigned char *comp=calloc(Nmax+1,1); comp[0]=comp[1]=1;
    for(u64 i=2;i*i<=Nmax;i++) if(!comp[i]) for(u64 k=i*i;k<=Nmax;k+=i) comp[k]=1;
    u64 cb=(u64)cbrtl((long double)Nmax*Nmax)+3; nsp=0; sp=malloc(sizeof(u64)*(cb+10));
    for(u64 i=2;i<=cb && i<=Nmax;i++) if(!comp[i]) sp[nsp++]=i;
    // candidates
    unsigned char *cand=calloc(Nmax+1,1); long ncand=0;
    for(u64 p=5;p<=Nmax;p++){ if(comp[p]||p%4!=1) continue; u64 pp=p*p;
        u64 r=0; for(u64 g=2;;g++){ r=powmod(g,(p-1)/4,p); if(mulmod(r,r,p)==p-1) break; }
        u64 t=( ((r*r+1)/p)%p ) * powmod((2*r)%p,p-2,p) % p; u64 R=(r+pp - (t*p)%pp)%pp;
        u64 roots[2]={R,pp-R};
        for(int z=0;z<2;z++) for(u64 n=roots[z];n<=Nmax;n+=pp) if(n) cand[n]=1; }
    for(u64 n=1;n<=Nmax;n++) ncand+=cand[n];
    fprintf(stderr,"Nmax=%llu K=%d candidates=%ld smallprimes=%d\n",Nmax,K,ncand,nsp);
    // global x matching
    matchX=malloc(sizeof(int)*(K+1)); matchA=malloc(sizeof(int)*(K+1)); vis=calloc(K+1,sizeof(int));
    for(int i=0;i<=K;i++){ matchX[i]=-1; matchA[i]=-1; }
    edge=malloc((size_t)(K+1)*NSH); memset(edge,-1,(size_t)(K+1)*NSH);
    int shift1=0;
    for(int j=1;j<=K;j++) if(has_edge(j,0) && matchA[j-1]<0){ matchX[j]=j-1; matchA[j-1]=j; shift1++; }
    int unmatched=0;
    for(int j=1;j<=K;j++) if(matchX[j]<0){ stamp++; if(!kuhn(j,0)) unmatched++; }
    fprintf(stderr,"x pairing: %d at shift -1, unmatched after augmenting: %d (x_0 left for plateau re-homing)\n",shift1,unmatched);
    // classes
    cls=calloc(K+1,sizeof(Cls));
    for(int m=0;m<=K;m++){ cls[m].v[cls[m].n++]=A(m); if(matchA[m]>=0) cls[m].v[cls[m].n++]=X(matchA[m]); }
    // y placement (greedy, increasing y, anchor <= y, nearest first)
    long ny=0,unpl=0; int W=400;
    int *ycls=NULL; u64 *yv=NULL; size_t ycap=ncand; ycls=malloc(sizeof(int)*ycap); yv=malloc(sizeof(u64)*ycap);
    for(u64 y=1;y<=Nmax;y++){ if(!cand[y]||y%25==7||y%25==18) continue;
        int b=(int)((y-7)/25); if(y<7){ unpl++; continue; } int placed=-1;
        for(int m=b;m>=0&&m>=b-W;m--){ Cls*c=&cls[m]; if(c->n>=CAP) continue; int ok=1;
            for(int i=0;i<c->n;i++) if(!is_sqfree(y*c->v[i]+1)){ ok=0; break; }
            if(ok){ c->v[c->n++]=y; placed=m; break; } }
        yv[ny]=y; ycls[ny]=placed; ny++; if(placed<0) unpl++; }
    fprintf(stderr,"other candidates: %ld, unplaced: %ld, sqfree tests so far %lld\n",ny,unpl,nsqtests);
    // per-plateau re-homing
    hmask=(1ULL<<22)-1; ht=calloc(hmask+1,sizeof(HE));
    parX=malloc(sizeof(int)*(K+1)); bq=malloc(sizeof(int)*(K+1)); lmA=malloc(sizeof(int)*(K+1)); lmX=malloc(sizeof(int)*(K+1)); lvis=calloc(K+1,sizeof(int));
    touchedA=malloc(sizeof(int)*(K+1)*2+64); touchedX=malloc(sizeof(int)*(K+1)*2+64);
    freeA=malloc(sizeof(int)*(K+1)); nfreeA=0; for(int m=0;m<=K;m++) if(matchA[m]<0) freeA[nfreeA++]=m;
    U=malloc(sizeof(int)*(K+1)); nU=0; for(int j=0;j<=K;j++) if(matchX[j]<0) U[nU++]=j;
    fprintf(stderr,"globally free anchors %d, unmatched x %d\n",nfreeA,nU);
    // local matching state = global matching restricted to the plateau
    for(int i=0;i<=K;i++){ lmA[i]=matchA[i]; lmX[i]=matchX[i]; }
    char fn[512]; snprintf(fn,sizeof fn,"%s/deltas.txt",od); FILE*fd=fopen(fn,"w");
    long fails=0,totmoves=0; int maxD=0;
    int *Dl=malloc(sizeof(int)*(K+1));
    for(int k=0;k<=K;k++){ curk=k; curN=25ULL*k+31; ntA=ntX=0;
        // anchors whose global partner is beyond the plateau are free; x's whose anchor is beyond are dangling
        int nD=0;
        for(int i=0;i<nU;i++){ if(U[i]>k) break; Dl[nD++]=U[i]; }
        for(int j=(k>=12?k-12:0);j<=k;j++){ int m=matchX[j]; if(m>k) Dl[nD++]=j; }
        for(int m=(k>=12?k-12:0);m<=k;m++) if(matchA[m]>k){ sA(m,-1); }
        for(int i=0;i<nD;i++){ int j=Dl[i]; if(lmX[j]>=0 && lmX[j]<=k) continue; sX(j,-1); }
        if(nD>maxD) maxD=nD;
        int ok=1;
        for(int i=0;i<nD;i++){ if(!lbfs(Dl[i])){ ok=0; break; } }
        if(!ok){ fails++; fprintf(fd,"%d FAIL\n",k); }
        else { // write moves: every x_j <= plateau whose local anchor differs from its global anchor
            fprintf(fd,"%d",k); int nm=0;
            for(int t=0;t<ntX;t++){ int j=touchedX[t]; if(j>k) continue; if(lmX[j]!=matchX[j] && lmX[j]>=0){ fprintf(fd," %d:%d",j,lmX[j]); nm++; lmX[j]=-2-lmX[j]; } }
            // restore markers
            for(int t=0;t<ntX;t++){ int j=touchedX[t]; if(lmX[j]<=-2) lmX[j]=-2-lmX[j]; }
            fprintf(fd,"\n"); totmoves+=nm; }
        // undo local changes
        for(int t=ntA-1;t>=0;t--){ int m=touchedA[t]; lmA[m]=matchA[m]; }
        for(int t=ntX-1;t>=0;t--){ int j=touchedX[t]; lmX[j]=matchX[j]; }
        if(k%100000==0) fprintf(stderr,"  plateau %d (N=%llu) fails so far %ld, tests %lld\n",k,curN,fails,nsqtests);
    }
    fclose(fd);
    // global assignment file: n anchor_index (anchors: own index; x's: global anchor or -1; others: class or -1)
    snprintf(fn,sizeof fn,"%s/global.txt",od); FILE*fg=fopen(fn,"w");
    fprintf(fg,"# Nmax %llu K %d\n",Nmax,K);
    long yi=0;
    for(u64 n=1;n<=Nmax;n++){ if(!cand[n]) continue;
        if(n%25==7) fprintf(fg,"%llu %llu\n",n,(n-7)/25);
        else if(n%25==18) fprintf(fg,"%llu %d\n",n,matchX[(n-18)/25]);
        else { while(yv[yi]!=n) yi++; fprintf(fg,"%llu %d\n",n,ycls[yi]); } }
    fclose(fg);
    int hist[CAP+1]={0}; for(int m=0;m<=K;m++) hist[cls[m].n]++;
    fprintf(stderr,"class sizes:"); for(int i=1;i<=CAP;i++) fprintf(stderr," %d:%d",i,hist[i]); fprintf(stderr,"\n");
    fprintf(stderr,"plateaus %d, failures %ld, max dangling %d, total re-homing moves %ld, sqfree tests %lld\n",K+1,fails,maxD,totmoves,nsqtests);
    return 0;
}
