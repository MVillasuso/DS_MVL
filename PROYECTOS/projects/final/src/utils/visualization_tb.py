import matplotlib.pyplot as plt
import seaborn as sns

def plot_img (l_img, l_lab, lfila, cnames):
    plt.figure(figsize=(10,10))
    for i in range(lfila*lfila):
        plt.subplot(lfila,lfila,i+1)
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        plt.imshow(l_img[i], cmap=plt.cm.binary)
        plt.xlabel(cnames[l_lab[i]])
    plt.show()