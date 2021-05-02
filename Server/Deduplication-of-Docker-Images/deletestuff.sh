rm -rf registry
rm -rf $1
rm image_index.json
rm metadata.json
rm -rf pop_registry
echo {"total":0} > popularity.json
echo {"images":[]} > list_pop_images.json
rm -rf cache/*
echo {} > cache.json