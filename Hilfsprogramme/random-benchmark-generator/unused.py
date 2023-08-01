def run_parallel_2(self, config_filename):
    def parallel_worker(width, height):
        nonlocal generated_benchmarks
        nonlocal maxOneHash
        nonlocal maxFailsCount
        nonlocal maxFailsLimitReached
        nonlocal maxFailsLimitCount
        nonlocal maxFailsLimit

        n = 0
        while n < countPerBenchmark:
            area_placer = AreaPlacer(width, height, min_pixel, max_pixel)
            final_grid = area_placer.place_areas()

            shapes = area_placer.generate_shapes(final_grid)
            benchmark = Benchmark(width, height, shapes)

            with lock:
                is_duplicate = any(are_benchmarks_equal(benchmark, existing_benchmark) for existing_benchmark in
                                   generated_benchmarks)

            lessThenThreshold = Main.shapes_with_less_hashes(benchmark, threshold)
            oneHash = Main.count_shapes_with_one_hash(benchmark)
            withinRange = Main.shapes_within_hash_range(benchmark, minThreshold, maxThreshold)

            if not is_duplicate and not withinRange and oneHash <= maxOneHash:
                with lock:
                    generated_benchmarks.add(benchmark)
                area_placer.save_benchmark(width, height, shapes, n, fileText, oneHash)
                n += 1
                maxFailsCount = 0
            else:
                maxFailsCount = maxFailsCount + 1
                if maxFailsCount > maxFailsLimit:
                    if maxFailsLimitReached < maxOneHashLimit:
                        maxFailsLimitReached = maxFailsLimitReached + 1
                        maxOneHash = maxOneHash + 1
                        maxFailsCount = 0
                        n = 0
                    else:
                        n = countPerBenchmark + 1
                        maxFailsCount = 0
                        maxFailsLimitReached = 0

    self.parse_args([config_filename])
    config_params = self.config_parameters
    self.configure_logging()

    # Assign the values from the configuration file to the respective variables
    minX, maxX = config_params["minX"], config_params["maxX"]
    minY, maxY = config_params["minY"], config_params["maxY"]
    min_pixel = config_params["min_pixel"]
    max_pixel = config_params["max_pixel"]
    threshold = config_params["threshold"]
    minThreshold = config_params["minThreshold"]
    maxThreshold = config_params["maxThreshold"]
    maxOneHashLimit = config_params["maxOneHash"]
    countPerBenchmark = config_params["countPerBenchmark"]
    maxFailsLimitReached = config_params["maxFailsLimitReached"]
    maxFailsLimitCount = config_params["maxFailsLimitCount"]
    maxFailsLimit = config_params["maxFailsLimit"]
    fileText = config_params["fileText"]
    maxFailsCount = config_params["maxFailsCount"]

    generated_benchmarks = set()
    maxOneHash = 1

    lock = threading.Lock()

    with ThreadPoolExecutor(max_workers=7) as executor:
        for width in range(minX, maxX + 1):
            for height in range(minY, maxY + 1):
                executor.submit(parallel_worker, width, height)

    print("Alle Aufgaben abgeschlossen.")


    def sendWAPP(self, message):
        self.send_whatsapp_message("+4915151373880", message)


    def send_whatsapp_message(self, phone_number, message):
        now = datetime.datetime.now()
        hour = now.hour
        minute = now.minute + 2  # Nachricht in zwei Minuten senden

        # Sendet die Nachricht über WhatsApp Web
        #kt.sendwhatmsg(phone_number, message, hour, minute, wait_time=30)