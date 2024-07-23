from building2parcel_trainingdata import Building2ParcelMapper

parcel_path = "C:/Million Neighborhoods/Spatial Data/ny-manhattan-parcels/NYC_2021_Tax_Parcels_SHP_2203/NewYork_2021_Tax_Parcels_SHP_2203.shp"
buildings_path = "C:/Million Neighborhoods/Spatial Data/ny-manhattan-buildings/geo_export_a80ea1a2-e8e0-4ffd-862c-1199433ac303.shp"

mapper = Building2ParcelMapper(parcel_path, buildings_path)

mapper.generate_images(
    parcel_images_directory='img/parcels',
    buildings_images_directory='img/buildings',
    combined_images_directory='img/combined',
    number_of_images=5
)