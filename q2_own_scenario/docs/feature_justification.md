# Q2 Feature Justification

                                                         feature                                            definition                                 decision
                                                        province              district mapped to one of five provinces      Coarse location known before choice
                                                        district                                          raw district      School location known before choice
                                                 school_category                                   raw school category        School type is public information
                                                combination_code                                  raw combination code    The programme the student is choosing
                                                ranking_category                            combination-to-section map                Programme family is known
                                                   gender_intake                                      raw intake label               Published admission policy
                                          olevel_avg_pct_2023_24                                 prior O-level results          Published before A-level choice
                                            olevel_rank_national                           prior national O-level rank          Published before A-level choice
                                                 olevel_rank_pct                         rank divided by 1,871 schools                    Normalised prior rank
                                               has_olevel_record                                 O-level value present           Records structural missingness
                                                  has_wda_record                                       WDA row present Records whether the school is WDA-listed
                                         wda_n_accredited_trades                    WDA trade count; 0 when not listed                    Accreditation breadth
                                                   wda_ownership         normalised WDA status; Not listed when absent              Ownership of listed schools
                                        n_combinations_at_school                            distinct offers per school                        Programme breadth
                                         alevel_rank_in_category Rank computed from the target within the NESA section                                  Leakage
                                    alevel_n_schools_in_category           Section size computed from the same results                                  Leakage
                                        school_code, school_name                                    Direct identifiers                               Identifier
                                       nesa_name_in_alevel_table                      Name matched from the NESA table                               Provenance
                       wda_sn, wda_match_score, wda_match_method                                 Record linkage fields                               Provenance
         wda_school_name, wda_province, wda_district, wda_sector                 Duplicates of known location/identity                               Provenance
                              district_code, sector_code, sector   Location identifiers; sector is finer than district                       Identifier/privacy
                                                   boarding_note                           Only two offers have a note                                 Unusable
                                                combination_name                    Duplicate text of combination_code                                Redundant
wda_accredited_trades, wda_accredited_levels, wda_non_accredited                                 Free-text trade lists                              Descriptive
