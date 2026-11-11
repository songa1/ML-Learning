# Feature Justification

                    feature created_or_keep_remove_reason                                         evidence linked_question
       fertilizer_kg_per_ha                       created Domain-informed feature engineering from Stage 5         B/C/D/E
             planting_month                       created Domain-informed feature engineering from Stage 5         B/C/D/E
           planting_quarter                       created Domain-informed feature engineering from Stage 5         B/C/D/E
     days_from_season_start                       created Domain-informed feature engineering from Stage 5         B/C/D/E
           is_improved_seed                       created Domain-informed feature engineering from Stage 5         B/C/D/E
                  seed_rank                       created Domain-informed feature engineering from Stage 5         B/C/D/E
              altitude_band                       created Domain-informed feature engineering from Stage 5         B/C/D/E
temp_deviation_from_optimum                       created Domain-informed feature engineering from Stage 5         B/C/D/E
              rain_per_temp                       created Domain-informed feature engineering from Stage 5         B/C/D/E
               rainfall_log                       created Domain-informed feature engineering from Stage 5         B/C/D/E
           fertilizer_log1p                       created Domain-informed feature engineering from Stage 5         B/C/D/E
              farm_size_log                       created Domain-informed feature engineering from Stage 5         B/C/D/E
             irrigated_flag                       created Domain-informed feature engineering from Stage 5         B/C/D/E
        season_x_irrigation                       created Domain-informed feature engineering from Stage 5         B/C/D/E
           planting_quarter                       removed                   Highly correlated pair |r|>0.9           A/B/C
              rain_per_temp                       removed                   Highly correlated pair |r|>0.9           A/B/C
               rainfall_log                       removed                   Highly correlated pair |r|>0.9           A/B/C
                 altitude_m                          kept   Selected by variance+f_regression on train set           A/B/C
              fertilizer_kg                          kept   Selected by variance+f_regression on train set           A/B/C
                 avg_temp_c                          kept   Selected by variance+f_regression on train set           A/B/C
                    soil_ph                          kept   Selected by variance+f_regression on train set           A/B/C
                 farmer_age                          kept   Selected by variance+f_regression on train set           A/B/C
               farm_size_ha                          kept   Selected by variance+f_regression on train set           A/B/C
                       year                          kept   Selected by variance+f_regression on train set           A/B/C
       fertilizer_kg_per_ha                          kept   Selected by variance+f_regression on train set           A/B/C
           is_improved_seed                          kept   Selected by variance+f_regression on train set           A/B/C
                  seed_rank                          kept   Selected by variance+f_regression on train set           A/B/C
temp_deviation_from_optimum                          kept   Selected by variance+f_regression on train set           A/B/C
           fertilizer_log1p                          kept   Selected by variance+f_regression on train set           A/B/C
              farm_size_log                          kept   Selected by variance+f_regression on train set           A/B/C
             irrigated_flag                          kept   Selected by variance+f_regression on train set           A/B/C
             low_yield_risk                          kept   Selected by variance+f_regression on train set           A/B/C

## Top Mutual Information

               feature  mutual_info
        low_yield_risk     0.497704
             seed_rank     0.131473
           rainfall_mm     0.073184
      is_improved_seed     0.030627
  fertilizer_kg_per_ha     0.028442
      fertilizer_log1p     0.026466
days_from_season_start     0.024836
            farmer_age     0.017455
         fertilizer_kg     0.015987
          farm_size_ha     0.008718
            altitude_m     0.000000
                  year     0.000000
            avg_temp_c     0.000000
               soil_ph     0.000000
        planting_month     0.000000

## RandomForest Importance (train only)

               feature  importance
        low_yield_risk    0.487865
             seed_rank    0.081624
  fertilizer_kg_per_ha    0.060119
            altitude_m    0.041148
            farmer_age    0.040682
               soil_ph    0.039961
days_from_season_start    0.039437
            avg_temp_c    0.029213
         rain_per_temp    0.027682
          farm_size_ha    0.020757
         farm_size_log    0.018782
      fertilizer_log1p    0.018265
           rainfall_mm    0.017928
          rainfall_log    0.017785
         fertilizer_kg    0.017735