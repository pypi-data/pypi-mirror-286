#ifndef _PASP_CMAP
#define _PASP_CMAP

#include <clingo.h>

#ifdef __cplusplus
extern "C" {
#endif

/** C wrapper for unordered_map<clingo_weighted_literal_t, int>. */
typedef struct map_wlit map_wlit_t;

map_wlit_t* map_wlit_create(size_t c);
void map_wlit_free(map_wlit_t *M);

/** Access key wlit in map M. */
int map_wlit_at(map_wlit_t *M, clingo_weighted_literal_t wlit);
/** Insert value v into M using key wlit. */
void map_wlit_insert(map_wlit_t *M, clingo_weighted_literal_t wlit, int v);

typedef struct {
  int bound;
  uint64_t level;
} ubound_t;

typedef struct map_ubound map_ubound_t;

map_ubound_t* map_ubound_create(size_t c);
void map_ubound_free(map_ubound_t *M);

/** Access key ubound in map M. */
int map_ubound_at(map_ubound_t *M, ubound_t b);
/** Insert value v into M using key ubound. */
void map_ubound_insert(map_ubound_t *M, ubound_t b, int v);

#ifdef __cplusplus
}
#endif

#endif
