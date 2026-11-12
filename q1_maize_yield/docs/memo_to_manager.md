# Memo to Manager

The revised Rwanda maize dataset contains 1,426 observations and 20 source columns. The Q1 workflow now uses `yield_t_ha` as the target and converts it to `yield_kg_per_ha`. It derives total fertiliser from NPK, urea and manure, uses `farm_area_ha`, and maps the pest index into an ordinal category. Missing values are handled by training-fitted preprocessing, and the source target is excluded from model inputs. The outputs are ready for later model evaluation, but this repository still does not train a production model.
