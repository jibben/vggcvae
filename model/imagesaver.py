from keras.callbacks import Callback
from matplotlib import pyplot as plt

class ImageSaver(Callback):
    ''' Keras Callback to save demo images after each epoch'''
    def __init__(self, image_path, images, shape, period=1, inp_path=None, out_path=None):
        self.images = images
        self.batch_size = images.shape[0]
        self.image_path = image_path
        self.shape = shape
        self.period = period
        self.inp_path = inp_path
        self.out_path = out_path

        self.dpi = 128
        self.fig_size = ((shape[0] * 4) // self.dpi, int(shape[1] * 1.5 * self.batch_size) // self.dpi)

        super(ImageSaver, self).__init__()

    def on_epoch_end(self, epoch, logs=None):
        if epoch % self.period == 0:
            vecs = self.model.layers[1].predict(self.images, batch_size=self.batch_size, verbose=0)
            pred = self.model.layers[2].predict(vecs, batch_size=self.batch_size, verbose=0)

            if inp_path and out_path:
                vecs.save(self.inp_path.format(epoch=epoch))
                pred.save(self.out_path.format(epoch=epoch))

            fig = plt.figure(figsize=self.fig_size)

            for i in range(self.batch_size):
                a = fig.add_subplot(self.batch_size, 2, i * 2 + 1)
                a.spines['top'].set_color('none')
                a.spines['bottom'].set_color('none')
                a.spines['left'].set_color('none')
                a.spines['right'].set_color('none')
                a.tick_params(labelcolor='w', top='off', bottom='off', left='off', right='off')
                img = plt.imshow(self.images[i].reshape(shape))
                a.set_title('input')

                a = fig.add_subplot(self.batch_size, 2, i * 2 + 2)
                a.spines['top'].set_color('none')
                a.spines['bottom'].set_color('none')
                a.spines['left'].set_color('none')
                a.spines['right'].set_color('none')
                a.tick_params(labelcolor='w', top='off', bottom='off', left='off', right='off')
                img = plt.imshow(pred[i].reshape(shape))
                a.set_title('decoded')

            fig.show()
            fig.savefig(self.image_path.format(epoch=epoch), bbox_inches='tight', dpi=self.dpi) 
