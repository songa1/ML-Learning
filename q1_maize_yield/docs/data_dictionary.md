# Data Dictionary

      column_name                    meaning    data_type           unit           allowed_values_or_notes known_to_be_post_harvest?
          farm_id                  Farm code       string            n/a                        identifier                        No
         province              Province name       string            n/a Eastern/Southern/Northern/Western                        No
         district              District name       string            n/a                    district label                        No
   cooperative_id           Cooperative code       string            n/a                            C001..                        No
       altitude_m              Farm altitude      numeric         meters                   approx 900-2800                        No
           season            Cropping season  categorical            n/a                             A/B/C                        No
    planting_date              Planting date         date           date                         2023-2025                        No
        farm_size            Farm size value numeric/text          mixed               with farm_size_unit                        No
   farm_size_unit             Farm size unit  categorical ha/m2/acre/are                     unit variants                        No
     seed_variety                  Seed type  categorical            n/a             Local/Improved/Hybrid                        No
    fertilizer_kg   Total fertilizer applied      numeric             kg                  whole farm total                        No
      rainfall_mm                   Rainfall      numeric             mm                 seasonal rainfall                        No
       avg_temp_c        Average temperature      numeric             °C                    season average                        No
        soil_type              Soil category  categorical            n/a                   Clay/Loam/Sandy                        No
          soil_ph                    Soil pH      numeric             pH                        approx 4-8                        No
   pest_incidence              Pest pressure      ordinal            n/a                   Low/Medium/High                        No
       irrigation            Irrigation used  categorical            n/a                            Yes/No                        No
       farmer_age                 Farmer age      numeric          years                    adult expected                        No
harvest_weight_kg             Harvest weight      numeric             kg         post-harvest leakage risk                       Yes
  yield_kg_per_ha Yield per hectare (target)      numeric          kg/ha                            target                       Yes