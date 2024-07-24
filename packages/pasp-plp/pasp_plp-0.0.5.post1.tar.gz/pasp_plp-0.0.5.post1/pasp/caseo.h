#ifndef _PASP_CASEO
#define _PASP_CASEO

#include <stdbool.h>
#include "cprogram.h"
#include "cinf.h"
#include "cdata.h"
#include "cmodels.h"

/**
 * Answer Set Enumeration by Optimality (ASEO).
 */

bool aseo(program_t *P, size_t k, psemantics_t psem, observations_t *O, int scale,
    size_t neural_idx, models_t* M, bool (*f)(const clingo_model_t*, program_t*, models_t*, size_t,
      observations_t*, clingo_control_t*), bool status);

bool aseo_reuse(program_t *P, size_t k, psemantics_t psem, observations_t *O, int scale,
    size_t neural_idx, clingo_weighted_literal_t *W, clingo_weighted_literal_t *U, models_t *M,
    bool (*f)(const clingo_model_t*, program_t*, models_t*, size_t,
      observations_t*, clingo_control_t*), bool status);

#endif
