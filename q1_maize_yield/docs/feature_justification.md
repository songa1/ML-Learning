# Q1 Feature Justification

                    feature     status                                         definition question
       fertilizer_kg_per_ha    Created    NPK + urea + manure converted to one kg/ha rate        B
           is_improved_seed    Created 1 when seed_variety is not Local; 0 for local seed        B
              altitude_band    Created                     Lowland, mid, or highland band        C
temp_deviation_from_optimum    Created                   Degrees outside the 18-27 C band        C
              rain_per_temp    Created            Rainfall divided by average temperature        C
               rainfall_log    Created                          Log transform of rainfall        C
           fertilizer_log1p    Created                   Log transform of fertiliser rate        B
              farm_size_log    Created                         Log transform of farm area        A
             irrigated_flag    Created               1 when irrigation is recorded as Yes        C
        season_x_irrigation    Created                     Season and irrigation combined      C/D
             low_yield_risk Label only      Bottom 20% of training yield; excluded from X        E
