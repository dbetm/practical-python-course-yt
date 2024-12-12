from PIL import Image

from ft_image import FTImage



if __name__ == "__main__":
    test_images_base_path = "sample-images"
    test_images_filenames = [
        "atardecer.ft",
        "flores.ft",
        "luna.ft",
        "noche-estrellada.ft",
    ]

    for filename in test_images_filenames:
        path = f"{test_images_base_path}/{filename}"
        img = FTImage(filepath=path)

        pillow_img = img.to_pil_image()
        pillow_img.show()

        x = input("Enter to continue...")

        # pillow_img = Image.open(path)
        # img = FTImage(img=pillow_img)

        # new_path = path.split(".")[0] + ".ft"
        # img.save(new_path)

    # img = FTImage(filepath="sample-images/simple.ft")
    # pillow_img = Image.open("sample-images/flores.jpg")

    # img = FTImage(img=pillow_img)

    # print(img)

    #img.save("sample-images/simple-copy.ft")

