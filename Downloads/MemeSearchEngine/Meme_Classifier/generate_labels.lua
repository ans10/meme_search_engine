require 'cunn'
require 'loadcaffe'
require 'optim'
require 'lfs'
require 'image'

function forward_image(vgg, image_path)
    im = image.load(image_path)
    siz = im:size()
    if siz[1] > 3 then
        im = im[{{1,3}}]
    elseif siz[1] < 3 then
        newim = torch.Tensor(3, siz[2], siz[3])
        newim[1] = im[1]
        newim[2] = im[1]
        newim[3] = im[1]
        im = newim
    end
    scaled = image.scale(im,224,224)
    scaled = scaled:cuda()
    scaled = scaled*256
    scaled[1] = scaled[1] - 123.68
    scaled[2] = scaled[2] - 116.779
    scaled[3] = scaled[3] - 103.939
    return vgg:forward(scaled)
end

vgg = loadcaffe.load('VGGNet/VGG_ILSVRC_19_layers_deploy.prototxt.txt','VGGNet/VGG_ILSVRC_19_layers.caffemodel')
vgg:cuda()
-- This is the output from Train_and_Test.ipynb
logistic = torch.load("memeclassifier")
-- This is the output from Feature_Generation.ipynb
data = torch.load("meme_features.t7")
classes = data[3]

f = io.open("labels", "w")
accumulator = 0

-- Modify the directory path to where your crawled images are located.
for file in lfs.dir("Search_Engine/common_image_base") do
    if lfs.attributes(file, "mode") ~= "directory" then
        status, result = pcall(forward_image, vgg, "Search_Engine/common_image_base/"..file)
        if not status then
            goto continue
        end
        features = vgg.modules[43].output
        newpred = logistic:forward(features)
        confidence, index = torch.max(newpred,1)
        if confidence[1] > 0.98 then
            print(file, classes[index[1]])
            accumulator = accumulator + 1
            f:write(accumulator.." "..file.." "..classes[index[1]])
            f:write('\n')
            f:flush()
        end
        ::continue::
    end
end
f:close()
