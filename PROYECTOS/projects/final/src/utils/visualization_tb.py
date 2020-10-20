import time
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import folders_tb as f_tb
from sklearn.metrics import classification_report, confusion_matrix

def plot_img (l_img, l_lab, lfila, cnames, dir_name, fname):
    plt.figure(figsize=(10,10))
    for i in range(lfila*lfila):
        plt.subplot(lfila,lfila,i+1)
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        plt.imshow(l_img[i], cmap=plt.cm.binary)
        plt.xlabel(cnames[l_lab[i]])
    f_tb.salvar_plot(dir_name,fname)
    plt.show()

def plot_history (history, dir_name, t_acc):
    print('[INFO] Generando gráfico...')
    plt.figure(figsize=(13,10))
    plt.style.use('ggplot')
    epoch_values = list(range(max(history.epoch)+1))
    plt.plot(epoch_values, history.history['loss'], label='Pérdida de entrenamiento')
    plt.plot(epoch_values, history.history['val_loss'], label='Pérdida de validación')
    plt.plot(epoch_values, history.history['accuracy'], label='Exactitud de entrenamiento')
    plt.plot(epoch_values, history.history['val_accuracy'], label='Exactitud de validación')
    plt.title('Pérdida y Exactitud de Entrenamiento')
    plt.xlabel('Epoch N°')
    plt.ylabel('Pérdida/Exactitud')
    plt.legend()
    moment=time.localtime()
    nfile = 'Grafico_{}_{}-{}-{}'.format(round(t_acc*100000),moment[2],moment[3],moment[4])
    f_tb.salvar_plot(dir_name,nfile)
    plt.show()

def plot_test  (ltest, llabels, lpredic, dim, cnames,dir_name, fname):
    plt.figure(figsize=(16,16))
    for i in range(dim*dim):
        plt.subplot(dim,dim,i+1)
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        plt.imshow(ltest[i], cmap=plt.cm.binary)
        pred_modelo = np.where(max(lpredic[i])==lpredic[i])[0][0]
        if cnames[llabels[i]] ==cnames[pred_modelo]:
            col='blue'
        else:
            col='red'
        plt.xlabel("Pred " +cnames[pred_modelo] +" " +str(round(max(lpredic[i])*100,2))+ "%",  color=col)
    f_tb.salvar_plot(dir_name,fname)
    plt.show()


def mat_confusion (predic, labels, cnames, dir_name,fname):
    pred = np.argmax(predic, axis=1)
    mc = confusion_matrix(labels, pred)
    df_mc = pd.DataFrame(mc, index= cnames, columns= cnames)
    df_mc.to_csv(dir_name+"/"+ fname, index = True)
    plt.figure(figsize=(8,5))  # Tamano de la imagen
    sns.set(font_scale=1.4)     # Tamano de la letra
    sns.heatmap(df_mc, annot=True, annot_kws={"size": 20}, cmap="Blues") 
    plt.ylabel('Real')          # Eje Y --> Valores reales
    plt.xlabel('Predicción')    # Eje X --> Valores de la predicción
    plt.title ("MATRIZ DE CONFUSIÓN")
    f_tb.salvar_plot(dir_name,fname)
    plt.show()
    return df_mc

def clasif_repor (predic, labels, cnames, dir_name, fname):
    pred = np.argmax(predic, axis=1)
    cr =classification_report(labels, pred, target_names=cnames, output_dict=True)
    #print(cr)
    df = pd.DataFrame.from_dict(cr).transpose()
    df.to_csv(dir_name+ "/"+ fname, index = True)
    return df