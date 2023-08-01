from jpgtopng import JPGToPNG
from zauberstab import Zauberstab
from maskapplier import MaskApplier
from concurrent.futures import ThreadPoolExecutor


class Main:
    def __init__(self):
        self.input_folder = "stickers"
        self.output_folder = "output_stickers"
        self.zauberstab_folder = "zauberstab_stickers"
        self.masked_folder = "masked_stickers"
        self.select_pixel_X = 0
        self.select_pixel_Y = 0
        self.toleranz = 5
        self.kontinuierlich = False
        self.muster = None
        self.anti_aliasing = True

    def run(self):
        remover = JPGToPNG(self.input_folder, self.output_folder)
        #remover.process_images()

        zauberstab = Zauberstab(toleranz = self.toleranz,
                                kontinuierlich = self.kontinuierlich,
                                muster = self.muster,
                                anti_aliasing = self.anti_aliasing)
        #zauberstab.bearbeite_bilder(input_folder = self.output_folder,
        #                            output_folder = self.zauberstab_folder,
        #                            x = self.select_pixel_X,
        #                            y = self.select_pixel_Y)

        maskapplier = MaskApplier()  # Create an instance of MaskApplier
        maskapplier.process_images(input_folder=self.output_folder,
                                   mask_folder=self.zauberstab_folder,
                                   output_folder=self.masked_folder)

    def run_parallel(self):
        remover = JPGToPNG(self.input_folder, self.output_folder)
        remover.process_images_parallel()

        zauberstab = Zauberstab(toleranz=self.toleranz,
                                kontinuierlich=self.kontinuierlich,
                                muster=self.muster,
                                anti_aliasing=self.anti_aliasing)
        zauberstab.bearbeite_bilder(input_folder=self.output_folder,
                                             output_folder=self.zauberstab_folder,
                                             x=self.select_pixel_X,
                                             y=self.select_pixel_Y)

        maskapplier = MaskApplier()  # Create an instance of MaskApplier
        maskapplier.process_images_parallel(input_folder=self.output_folder,
                                            mask_folder=self.zauberstab_folder,
                                            output_folder=self.masked_folder)


if __name__ == '__main__':
    main = Main()
    main.run_parallel()