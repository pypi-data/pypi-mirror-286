#include "cmap.hh"

#include <unordered_map>

struct cmap_hash_wlit {
  std::size_t operator() (const clingo_weighted_literal_t &wlit) const {
    auto u = std::hash<clingo_literal_t>{}(wlit.literal);
    auto v = std::hash<clingo_weight_t>{}(wlit.weight);
    return u ^ (v + 0x9e3779b9 + (u << 6) + (u >> 2));
  }
};

struct cmap_equal_wlit {
  bool operator() (const clingo_weighted_literal_t &lhs, const clingo_weighted_literal_t &rhs) const {
    return lhs.literal == rhs.literal && lhs.weight == rhs.weight;
  }
};

struct map_wlit {
  std::unordered_map<clingo_weighted_literal_t, int, cmap_hash_wlit, cmap_equal_wlit> umap;
  map_wlit(size_t c) : umap(c) {};
};

map_wlit_t* map_wlit_create(size_t c) { return new map_wlit_t(c); }
void map_wlit_free(map_wlit_t *M) { delete M; }

int map_wlit_at(map_wlit_t *M, clingo_weighted_literal_t wlit) { return (M->umap)[wlit]; }
void map_wlit_insert(map_wlit_t *M, clingo_weighted_literal_t wlit, int v) { (M->umap)[wlit] = v; }

struct cmap_hash_ubound {
  std::size_t operator() (const ubound_t &b) const {
    auto u = std::hash<int>{}(b.bound);
    auto v = std::hash<uint64_t>{}(b.level);
    return u ^ (v + 0x9e3779b9 + (u << 6) + (u >> 2));
  }
};

struct cmap_equal_ubound {
  bool operator() (const ubound_t &lhs, const ubound_t &rhs) const {
    return lhs.bound == rhs.bound && lhs.level == rhs.level;
  }
};

struct map_ubound {
  std::unordered_map<ubound_t, int, cmap_hash_ubound, cmap_equal_ubound> umap;
  map_ubound(size_t c) : umap(c) {};
};

map_ubound_t* map_ubound_create(size_t c) { return new map_ubound_t(c); }
void map_ubound_free(map_ubound_t *M) { delete M; }

int map_ubound_at(map_ubound_t *M, ubound_t b) { return (M->umap)[b]; }
void map_ubound_insert(map_ubound_t *M, ubound_t b, int v) { (M->umap)[b] = v; }
