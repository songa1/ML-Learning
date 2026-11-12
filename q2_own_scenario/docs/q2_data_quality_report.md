# Q2 Data Quality Report

                                    problem                                      columns_affected  records_affected severity                     proposed_treatment
                       Exact duplicate rows                                           all columns                 0     High                  Remove identical rows
        Duplicate school x combination rows                         school_code, combination_code                 0     High                     Keep one offer row
          Offers without the A-level target                                alevel_avg_pct_2023_24                53     High            Drop; cannot supervise them
           Offers without an O-level record          olevel_avg_pct_2023_24, olevel_rank_national               607   Medium       Keep; add has_olevel_record flag
                Offers without a WDA record                         wda_sn and other wda_* fields               817   Medium          Keep; add has_wda_record flag
             Offers without a boarding note                                         boarding_note              1276      Low Exclude the field; too sparse to model
                    WDA ownership spellings                                            wda_status                13   Medium                Map to Public / Private
            Columns derived from the target alevel_rank_in_category, alevel_n_schools_in_category                 2     High              Exclude from model inputs
                           Constant columns                               olevel_n_schools_ranked                 1      Low       Drop after deriving rank percent
Combination codes without a ranking section                                      combination_code                 0     High           Investigate before modelling
            Target values outside 1.5 x IQR                                alevel_avg_pct_2023_24                 8      Low          Keep; report rather than clip
 School names with repeated internal spaces                                           school_name                23      Low                    Collapse whitespace
