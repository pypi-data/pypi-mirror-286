#ifndef _PASP_CTHREAD
#define _PASP_CTHREAD

#include <stdlib.h>
#include <pthread.h>
#include <stdbool.h>

#include "cinf.h"

#ifndef NUM_PROCS
#define NUM_PROCS 1
#endif

typedef struct {
  pthread_t T[NUM_PROCS];
  bool busy[NUM_PROCS];
  storage_t *data;
  pthread_mutex_t wakeup;
  pthread_cond_t avail;
  size_t n;
} pool_t;

pool_t* pool_create(size_t n, storage_t *data);
bool pool_init(pool_t *P, size_t n, storage_t *data);

void pool_free_contents(pool_t *P);
void pool_free(pool_t *P);

int pool_find_id(pool_t *P);

bool pool_spawn(pool_t *Q, void* (*f)(void*), total_choice_t *theta);
bool pool_spawn_payload(pool_t *Q, void* (*f)(void*), total_choice_t *theta, int id, void *payload);

void pool_wait(pool_t *P);

#endif
