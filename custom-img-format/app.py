from PIL import Image

from ft_img import FTImage


if __name__ == "__main__":
    #img = FTImage(filepath="sample-images/test_compressed.ft")

    pillow_img = Image.open("sample-images/flores.jpg")
    img = FTImage(img=pillow_img)

    print(img)

    #img.save("sample-images/test2_compressed.ft")

    # img.change_bright(100)

    #pillow_img = img.to_pil_image()

    #pillow_img.show()

    #img.change_bright(42)
    #print("-"*32)
    #print(img)
    img.save("sample-images/flores_compressed.ft")