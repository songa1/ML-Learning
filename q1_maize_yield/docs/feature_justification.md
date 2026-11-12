# Q1 Feature Justification

| Feature | Decision | Reason |
|---|---|---|
| `fertilizer_kg` | Derived | Combines NPK and urea in kg/ha with manure converted from tonnes/ha to kg/ha. |
| `fertilizer_kg_per_ha` | Kept | The revised source fertiliser fields are already normalised by hectare. |
| `is_improved_seed` | Created | Encodes the improved/traditional farming-practice distinction. |
| `seed_rank` | Created | Provides a simple ordered indicator for the practice category. |
| `altitude_band` | Created | Represents broad elevation zones for agronomic comparison. |
| `temp_deviation_from_optimum` | Created | Measures distance outside the assumed 18–27°C suitable range. |
| `rain_per_temp` | Created | Relates rainfall to temperature while retaining both source measurements. |
| `rainfall_log`, `fertilizer_log1p`, `farm_size_log` | Created | Reduces skew in heavily tailed measurements. |
| `irrigated_flag` | Created | Encodes irrigation status numerically. |
| `season_x_irrigation` | Created | Captures a possible interaction between season and irrigation. |
| `yield_t_ha` | Excluded | Source target; including it would leak the answer into the model. |
