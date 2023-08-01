class MonsterRuntime:
    def __init__(self, runtimes=None):
        self.runtime_nr_1369 = None
        self.runtime_name_1369 = None
        self.runtime_total_sec_1369 = None
        self.runtime_seconds_1369 = None
        self.runtime_minutes_1369 = None
        self.runtime_hours_1369 = None
        self.runtime_days_1369 = None

        self.runtime_nr_1370 = None
        self.runtime_name_1370 = None
        self.runtime_total_sec_1370 = None
        self.runtime_seconds_1370 = None
        self.runtime_minutes_1370 = None
        self.runtime_hours_1370 = None
        self.runtime_days_1370 = None

        self.runtime_nr_1371 = None
        self.runtime_name_1371 = None
        self.runtime_total_sec_1371 = None
        self.runtime_seconds_1371 = None
        self.runtime_minutes_1371 = None
        self.runtime_hours_1371 = None
        self.runtime_days_1371 = None

        self.runtime_nr_1372 = None
        self.runtime_name_1372 = None
        self.runtime_total_sec_1372 = None
        self.runtime_seconds_1372 = None
        self.runtime_minutes_1372 = None
        self.runtime_hours_1372 = None
        self.runtime_days_1372 = None

        self.runtime_nr_1373 = None
        self.runtime_name_1373 = None
        self.runtime_total_sec_1373 = None
        self.runtime_seconds_1373 = None
        self.runtime_minutes_1373 = None
        self.runtime_hours_1373 = None
        self.runtime_days_1373 = None

        self.runtime_nr_1374 = None
        self.runtime_name_1374 = None
        self.runtime_total_sec_1374 = None
        self.runtime_seconds_1374 = None
        self.runtime_minutes_1374 = None
        self.runtime_hours_1374 = None
        self.runtime_days_1374 = None

        self.runtime_nr_1375 = None
        self.runtime_name_1375 = None
        self.runtime_total_sec_1375 = None
        self.runtime_seconds_1375 = None
        self.runtime_minutes_1375 = None
        self.runtime_hours_1375 = None
        self.runtime_days_1375 = None

        self.runtime_nr_1376 = None
        self.runtime_name_1376 = None
        self.runtime_total_sec_1376 = None
        self.runtime_seconds_1376 = None
        self.runtime_minutes_1376 = None
        self.runtime_hours_1376 = None
        self.runtime_days_1376 = None

        self.runtime_nr_1377 = None
        self.runtime_name_1377 = None
        self.runtime_total_sec_1377 = None
        self.runtime_seconds_1377 = None
        self.runtime_minutes_1377 = None
        self.runtime_hours_1377 = None
        self.runtime_days_1377 = None

        if runtimes:
            for runtime in runtimes:
                if runtime.runtime_nr == "1369":
                    self.runtime_nr_1369 = 1369
                    self.runtime_name_1369 = runtime.runtime_name
                    self.runtime_total_sec_1369 = runtime.total_sec
                    self.runtime_seconds_1369 = runtime.runtime_seconds
                    self.runtime_minutes_1369 = runtime.runtime_minutes
                    self.runtime_hours_1369 = runtime.runtime_hours
                    self.runtime_days_1369 = runtime.runtime_days
                elif runtime.runtime_nr == "1370":
                    self.runtime_nr_1370 = 1370
                    self.runtime_name_1370 = runtime.runtime_name
                    self.runtime_total_sec_1370 = runtime.total_sec
                    self.runtime_seconds_1370 = runtime.runtime_seconds
                    self.runtime_minutes_1370 = runtime.runtime_minutes
                    self.runtime_hours_1370 = runtime.runtime_hours
                    self.runtime_days_1370 = runtime.runtime_days
                elif runtime.runtime_nr == "1371":
                    self.runtime_nr_1371 = 1371
                    self.runtime_name_1371 = runtime.runtime_name
                    self.runtime_total_sec_1371 = runtime.total_sec
                    self.runtime_seconds_1371 = runtime.runtime_seconds
                    self.runtime_minutes_1371 = runtime.runtime_minutes
                    self.runtime_hours_1371 = runtime.runtime_hours
                    self.runtime_days_1371 = runtime.runtime_days
                elif runtime.runtime_nr == "1372":
                    self.runtime_nr_1372 = 1372
                    self.runtime_name_1372 = runtime.runtime_name
                    self.runtime_total_sec_1372 = runtime.total_sec
                    self.runtime_seconds_1372 = runtime.runtime_seconds
                    self.runtime_minutes_1372 = runtime.runtime_minutes
                    self.runtime_hours_1372 = runtime.runtime_hours
                    self.runtime_days_1372 = runtime.runtime_days
                elif runtime.runtime_nr == "1373":
                    self.runtime_nr_1373 = 1373
                    self.runtime_name_1373 = runtime.runtime_name
                    self.runtime_total_sec_1373 = runtime.total_sec
                    self.runtime_seconds_1373 = runtime.runtime_seconds
                    self.runtime_minutes_1373 = runtime.runtime_minutes
                    self.runtime_hours_1373 = runtime.runtime_hours
                    self.runtime_days_1373 = runtime.runtime_days
                elif runtime.runtime_nr == "1374":
                    self.runtime_nr_1374 = 1374
                    self.runtime_name_1374 = runtime.runtime_name
                    self.runtime_total_sec_1374 = runtime.total_sec
                    self.runtime_seconds_1374 = runtime.runtime_seconds
                    self.runtime_minutes_1374 = runtime.runtime_minutes
                    self.runtime_hours_1374 = runtime.runtime_hours
                    self.runtime_days_1374 = runtime.runtime_days
                elif runtime.runtime_nr == "1375":
                    self.runtime_nr_1375 = 1375
                    self.runtime_name_1375 = runtime.runtime_name
                    self.runtime_total_sec_1375 = runtime.total_sec
                    self.runtime_seconds_1375 = runtime.runtime_seconds
                    self.runtime_minutes_1375 = runtime.runtime_minutes
                    self.runtime_hours_1375 = runtime.runtime_hours
                    self.runtime_days_1375 = runtime.runtime_days
                elif runtime.runtime_nr == "1376":
                    self.runtime_nr_1376 = 1376
                    self.runtime_name_1376 = runtime.runtime_name
                    self.runtime_total_sec_1376 = runtime.total_sec
                    self.runtime_seconds_1376 = runtime.runtime_seconds
                    self.runtime_minutes_1376 = runtime.runtime_minutes
                    self.runtime_hours_1376 = runtime.runtime_hours
                    self.runtime_days_1376 = runtime.runtime_days
                elif runtime.runtime_nr == "1377":
                    self.runtime_nr_1377 = 1377
                    self.runtime_name_1377 = runtime.runtime_name
                    self.runtime_total_sec_1377 = runtime.total_sec
                    self.runtime_seconds_1377 = runtime.runtime_seconds
                    self.runtime_minutes_1377 = runtime.runtime_minutes
                    self.runtime_hours_1377 = runtime.runtime_hours
                    self.runtime_days_1377 = runtime.runtime_days

    def __str__(self):
        return f"Runtime 1369: nr={self.runtime_nr_1369}, name={self.runtime_name_1369}, total_sec={self.runtime_total_sec_1369}, seconds={self.runtime_seconds_1369}, minutes={self.runtime_minutes_1369}, hours={self.runtime_hours_1369}, days={self.runtime_days_1369}, \n" \
               f"Runtime 1370: nr={self.runtime_nr_1370}, name={self.runtime_name_1370}, total_sec={self.runtime_total_sec_1370}, seconds={self.runtime_seconds_1370}, minutes={self.runtime_minutes_1370}, hours={self.runtime_hours_1370}, days={self.runtime_days_1370}, \n" \
               f"Runtime 1371: nr={self.runtime_nr_1371}, name={self.runtime_name_1371}, total_sec={self.runtime_total_sec_1371}, seconds={self.runtime_seconds_1371}, minutes={self.runtime_minutes_1371}, hours={self.runtime_hours_1371}, days={self.runtime_days_1371}, \n" \
               f"Runtime 1372: nr={self.runtime_nr_1372}, name={self.runtime_name_1372}, total_sec={self.runtime_total_sec_1372}, seconds={self.runtime_seconds_1372}, minutes={self.runtime_minutes_1372}, hours={self.runtime_hours_1372}, days={self.runtime_days_1372}, \n" \
               f"Runtime 1373: nr={self.runtime_nr_1373}, name={self.runtime_name_1373}, total_sec={self.runtime_total_sec_1373}, seconds={self.runtime_seconds_1373}, minutes={self.runtime_minutes_1373}, hours={self.runtime_hours_1373}, days={self.runtime_days_1373}, \n" \
               f"Runtime 1374: nr={self.runtime_nr_1374}, name={self.runtime_name_1374}, total_sec={self.runtime_total_sec_1374}, seconds={self.runtime_seconds_1374}, minutes={self.runtime_minutes_1374}, hours={self.runtime_hours_1374}, days={self.runtime_days_1374}, \n" \
               f"Runtime 1375: nr={self.runtime_nr_1375}, name={self.runtime_name_1375}, total_sec={self.runtime_total_sec_1375}, seconds={self.runtime_seconds_1375}, minutes={self.runtime_minutes_1375}, hours={self.runtime_hours_1375}, days={self.runtime_days_1375}, \n" \
               f"Runtime 1376: nr={self.runtime_nr_1376}, name={self.runtime_name_1376}, total_sec={self.runtime_total_sec_1376}, seconds={self.runtime_seconds_1376}, minutes={self.runtime_minutes_1376}, hours={self.runtime_hours_1376}, days={self.runtime_days_1376}, \n" \
               f"Runtime 1377: nr={self.runtime_nr_1377}, name={self.runtime_name_1377}, total_sec={self.runtime_total_sec_1377}, seconds={self.runtime_seconds_1377}, minutes={self.runtime_minutes_1377}, hours={self.runtime_hours_1377}, days={self.runtime_days_1377}"
