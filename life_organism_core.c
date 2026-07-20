#include <string.h>
typedef struct { unsigned long long k; char v[32]; int l, active; } Fact;
Fact db[1000];
long long tick(long long n) { return n <= 1 ? 1 : (n % 2 == 0 ? n / 2 : 3 * n + 1); }
unsigned long long hash(unsigned long long k) {
    unsigned long long h = 1469598103934665603ULL;
    for(int i=0; i<8; i++) { h ^= ((unsigned char*)&k)[i]; h *= 1099511628211ULL; }
    return h;
}
void observe(unsigned long long k, const char* v) {
    for (int i = 0; i < 1000; i++) {
        if (db[i].active && db[i].k == k) { db[i].l = 27 + (hash(k) % 80); return; }
    }
    for (int i = 0; i < 1000; i++) {
        if (!db[i].active) {
            db[i].k = k; strcpy(db[i].v, v); db[i].l = 27 + (hash(k) % 80); db[i].active = 1; return;
        }
    }
}
const char* recall(unsigned long long k) {
    for (int i = 0; i < 1000; i++) {
        if (db[i].active && db[i].k == k) return db[i].v;
    }
    return "ABSTAIN";
}
void heartbeat() {
    for (int i = 0; i < 1000; i++) {
        if (db[i].active && (db[i].l = tick(db[i].l)) <= 1) db[i].active = 0;
    }
}
