class ModelInputs:
    def __init__(self, project_name, drilled_after, drilled_before, provinces, formations, horizontal, min_gor, max_gor, **kwargs):
        # Initialize the ModelInputs class with core attributes
        self.project_name = project_name
        self.drilled_after = drilled_after
        self.drilled_before = drilled_before
        self.provinces = provinces
        self.formations = formations
        self.horizontal = horizontal
        self.min_gor = min_gor
        self.max_gor = max_gor

        # Dynamically assign additional keyword arguments to the instance
        for key, value in kwargs.items():
            setattr(self, key, value) # Set additional attributes as needed from kwargs

        # self.prod_data_checkbox = prod_data_checkbox
        # self.inject_data_checkbox = inject_data_checkbox
        # self.fluid_data_checkbox = fluid_data_checkbox
        # self.pressure_DST_data_checkbox = pressure_DST_data_checkbox
        # self.HF_water_checkbox = HF_water_checkbox
        # self.facility_data_checkbox = facility_data_checkbox
        # self.OPGEE_distribution_checkbox = OPGEE_distribution_checkbox
        # self.OPGEE_export_checkbox = OPGEE_export_checkbox

    def __str__(self):
        # Generate a string representation of the core attributes of the instance
        base_info = (f"Project Name: {self.project_name}\n"
                f"Drilled After Date: {self.drilled_after}\n"
                f"Drilled Before Date: {self.drilled_before}\n"
                f"Provinces of Interest: {self.provinces}\n"
                f"Formations of Interest: {self.formations}\n"
                f"Horizontal Well: {self.horizontal}\n"
                f"Minimum First 12 month Ave GOR: {self.min_gor}\n"
                f"Maximum First 12 month Ave GOR: {self.max_gor}\n"
                # f"Production Data: {self.prod_data_checkbox}\n"
                # f"Injection Data: {self.inject_data_checkbox}\n"
                # f"Fluid Data: {self.fluid_data_checkbox}\n"
                # f"Pressure/DST Data: {self.pressure_DST_data_checkbox}\n"
                # f"HF Water Data: {self.HF_water_checkbox}\n"
                # f"Facility Data: {self.facility_data_checkbox}\n"
                # f"OPGEE Distribution Parameters: {self.OPGEE_distribution_checkbox}\n"
                # f"Export to OPGEE: {self.OPGEE_export_checkbox}"
        )
        # Append any additional dynamically set attributes to the string
        additional_info = ""
        for key, value in vars(self).items():
            if key not in ["project_name", "drilled_after", "drilled_before", "provinces", "formations", "horizontal", "min_gor", "max_gor"]:
                additional_info += f"{key.replace('_', ' ').title()}: {value}\n"

        return base_info + additional_info # Return the combined string representation of the instance       

# # Module-level variable to store the instance
# inputs_instance = None
