#include "cthread.h"

#include <string.h>

pool_t* pool_create(size_t n, storage_t *data) {
  pool_t *P = (pool_t*) malloc(sizeof(pool_t));
  if (!P) return NULL;
  if (!pool_init(P, n, data)) return NULL;
  return P;
}

bool pool_init(pool_t *P, size_t n, storage_t *data) {
  P->n = n; P->data = data;
  if (pthread_mutex_init(&P->wakeup, NULL)) return false;
  if (pthread_cond_init(&P->avail, NULL)) return false;
  memset(P->busy, 0, n*sizeof(bool));
  return true;
}

void pool_free_contents(pool_t *P) {
  pthread_mutex_destroy(&P->wakeup);
  pthread_cond_destroy(&P->avail);
}
void pool_free(pool_t *P) { pool_free_contents(P); free(P); }

int pool_find_id(pool_t *P) {
  int i, id = -1;
  pthread_mutex_lock(&P->wakeup);
  while (true) {
    for (i = 0, id = -1; i < P->n; ++i) if (!P->busy[i]) { id = i; break; }
    if (id != -1) break;
    pthread_cond_wait(&P->avail, &P->wakeup);
  }
  P->busy[id] = true;
  pthread_mutex_unlock(&P->wakeup);
  return id;
}

bool pool_spawn(pool_t *P, void* (*f)(void*), total_choice_t *theta) {
  int id = pool_find_id(P);
  copy_total_choice(theta, &P->data[id].theta);
  return !(P->data[id].fail || pthread_create(&P->T[id], NULL, f, &P->data[id]));
}
bool pool_spawn_payload(pool_t *P, void* (*f)(void*), total_choice_t *theta, int id, void *payload) {
  copy_total_choice(theta, &P->data[id].theta);
  return !(P->data[id].fail || pthread_create(&P->T[id], NULL, f, payload));
}

void pool_wait(pool_t *P) {
  for (size_t i = 0; i < P->n; ++i) pthread_join(P->T[i], NULL);
}
