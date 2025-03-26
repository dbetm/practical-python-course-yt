from PIL import Image

from ft_image import FTImage, FTImage2



if __name__ == "__main__":
    test_images_base_path = "sample-images"
    test_images_filenames = [
        "atardecer_v2.ft",
        "flores_v2.ft",
        "luna_v2.ft",
        "noche-estrellada_v2.ft",
    ]

    for filename in test_images_filenames:
        path = f"{test_images_base_path}/{filename}"
        img = FTImage2(filepath=path)

        pillow_img = img.to_pil_image()
        pillow_img.show()

        x = input("Enter to continue...")

        # pillow_img = Image.open(path)
        # img = FTImage2(img=pillow_img)

        # new_path = path.split(".")[0] + "_v2.ft"
        # img.save(new_path)

    #img = FTImage(filepath="sample-images/simple.ft")
    # pillow_img = Image.open("sample-images/flores.jpg")

    # img = FTImage(img=pillow_img)

    # print(img)

    # img.save("sample-images/flores.ft")