class ModelInputs:
    def __init__(self, drilled_after, drilled_before, provinces, formations, horizontal, min_gor, max_gor): # removed start_date and end_date
        self.drilled_after = drilled_after
        self.drilled_before = drilled_before
        self.provinces = provinces
        self.formations = formations
        self.horizontal = horizontal
        self.min_gor = min_gor
        self.max_gor = max_gor
        # self.start_date = start_date
        # self.end_date = end_date

    def __str__(self):
        return (f"Drilled After Date: {self.drilled_after}\n"
                f"Drilled Before Date: {self.drilled_before}\n"
                f"Provinces of Interest: {self.provinces}\n"
                f"Formations of Interest: {self.formations}\n"
                f"Horizontal Well: {self.horizontal}\n"
                f"Minimum First 12 month Ave GOR: {self.min_gor}\n"
                f"Maximum First 12 month Ave GOR: {self.max_gor}\n"
                # f"Start Date: {self.start_date}\n"
                # f"End Date: {self.end_date}")
        )

# Module-level variable to store the instance
inputs_instance = None
