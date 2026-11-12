# Q1 Data Quality Report

                    problem                         columns_affected  records_affected severity                                  proposed_treatment
       Exact duplicate rows                                      all                 0     High                             Remove exact duplicates
Repeated record identifiers                                record_id                 0     High                       Keep the most complete record
             Missing values rainfall_mm,soil_ph,pest_incidence_index                 0   Medium                          Fit training-only imputers
     Invalid target or area                  yield_t_ha,farm_area_ha                 0     High Set invalid values missing and drop missing targets
    Out-of-range pest index                     pest_incidence_index                 0   Medium                          Set invalid values missing
   Potential target leakage                               yield_t_ha              1426     High          Keep only as target; never include it in X