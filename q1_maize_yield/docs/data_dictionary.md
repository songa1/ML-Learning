# Q1 Data Dictionary

         column_name                meaning data_type                          unit post_harvest_or_target
           record_id Observation identifier    string            unique record code                     No
                year       Observation year   integer                     2015-2030                     No
              season        Cropping season  category                         A/B/C                     No
            province               Province  category               Rwanda province                     No
            district               District  category               Rwanda district                     No
          altitude_m               Altitude   numeric                        metres                     No
         rainfall_mm               Rainfall   numeric                   millimetres                     No
          avg_temp_c    Average temperature   numeric               degrees Celsius                     No
             soil_ph           Soil acidity   numeric                            pH                     No
           soil_type          Soil category  category                    soil class                     No
        seed_variety           Seed variety  category                 variety label                     No
    farming_practice       Farming practice  category          Traditional/Improved                     No
           npk_kg_ha         NPK fertiliser   numeric                         kg/ha                     No
          urea_kg_ha        Urea fertiliser   numeric                         kg/ha                     No
         manure_t_ha                 Manure   numeric                     tonnes/ha                     No
plant_density_per_ha          Plant density   numeric                     plants/ha                     No
        farm_area_ha              Farm area   numeric                      hectares                     No
          irrigation             Irrigation  category                        Yes/No                     No
pest_incidence_index   Pest incidence index   numeric                     0-1 index                     No
          yield_t_ha           Yield target   numeric tonnes/ha; converted to kg/ha                    Yes