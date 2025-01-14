import cv2

#rastreador = cv2.legacy.TrackerKCF_create()
rastreador = cv2.legacy.TrackerCSRT_create()

video = cv2.VideoCapture('street.mp4')
ok, frame = video.read()

box = cv2.selectROI(frame) # Region of interest

ok = rastreador.init(frame, box)

while True:

    ok, frame = video.read()

    if not ok:
        break

    #Atualiza o box
    ok, box = rastreador.update(frame)

    if ok:
        #Obtendo as coordenadas do ROI
        (x, y, w, h) = [int(v) for v in box]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2, 1)
    else:
        #Caso o rastreamento falhe
        cv2.putText(frame, 'Erro', (100,80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


    # Mostra o quadro
    cv2.imshow('Rastreamento', frame)

    #Sair do loop quando a tecla for pressionada
    if cv2.waitKey(1) & 0XFF == 27: #ESC
        break

