from PIL import Image, ImageDraw, ImageFont
from matplotlib.pylab import *
import matplotlib.cm as cm
from matplotlib.colors import LinearSegmentedColormap
import textwrap




def create_logo(inputimage, kgCO2eq) :
	########### Définir les couleurs du logo ###########
	# -----Définir l'échelle de couleur -----
	green = (122, 237, 3)
	yellow = (255, 204, 0)
	orange = (240,131, 0)
	red = (255, 58, 50)
	violet = (255, 0, 0)
	G = (green[0]/255, green[1]/255, green[2]/255)
	Y = (yellow[0]/255, yellow[1]/255, yellow[2]/255)
	O = (orange[0]/255, orange[1]/255, orange[2]/255)
	R = (red[0]/255, red[1]/255, red[2]/255)
	V = (violet[0]/255, violet[1]/255, violet[2]/255)
	colors = [G, Y, O, R, V]  # G -> Y -> R
	n_bin = 256 
	cmap_name = 'my_list'
	colorscale = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bin)
	min_val=0
	max_val=5.5
	cmap = cm.get_cmap(colorscale)
	norm=matplotlib.colors.Normalize(min_val,max_val)
	color=cmap(norm(kgCO2eq)) 
	r = int(color[0]*255)
	g = int(color[1]*255)
	b = int(color[2]*255)
	a = int(color[3]*255)
	color = (r,g,b,a) #couleur du logo
	colortext=(0,0,0,255) #couleur du texte

	######### Importer logo en transparence et le superposer à un fond coloré #########
	im2 = Image.open(inputimage) 
	im1 = Image.new("RGBA", im2.size, color)
	logo=Image.alpha_composite(im1,im2)
	draw = ImageDraw.Draw(logo)
	########### Dessin de la jauge ###########
	# ----- Arc de gauche de la jauge (fixe) -----
	x01, y01 = 276, 258
	x02, y02 = 335, 319
	# ----- Arc de droite de la jauge (variable) -----
	#coordonnées de l'arc de droite de la jauge noire
	x03, y03 = 1364, y01
	x04, y04 = 1423, y02
	#coordonnées à calculer selon la valeur en kgCO2eq)
	lx = x04-x03
	xa1, ya1 = x01+(x04-x01)*min(kgCO2eq,5.5)/5.5-lx, y01
	xa2, ya2 = x01+(x04-x01)*min(kgCO2eq,5.5)/5.5, y02
	# ----- Rectangle de la jauge -----
	#coordonnées pour le rectangle (dépendent de la position des arcs)
	xr1, yr1 = (x01+x02)/2, y01
	xr2, yr2 = (xa1+xa2)/2, y02
	# ----- Dessin jauge intérieure
	if xa1>x01 :
		draw.chord([(x01,y01),(x02,y02)],90,-90,outline=color,fill=color)
		draw.chord([(xa1,ya1),(xa2,ya2)],-90,90,outline=color,fill=color)
		draw.rectangle([(xr1,yr1),(xr2,yr2)], fill=color) 
	else : 
		draw.chord([(x01,y01),(x02,y02)],90,-90,outline=color,fill=color)
		#draw.chord([(xa1,ya1),(xa2,ya2)],-90,90,outline=color,fill=color)	

	########### Dessin valeurs ###########
	# ----- Texte valeur kgCO2eq -----
	kgeq=round(kgCO2eq,1) #valeur arrondie au dixième
	xkg, ykg = 100, 125
	font1 = ImageFont.truetype("./static/font/Lato-Regular.ttf", size=100)
	draw.text((xkg, ykg), str(kgeq), font=font1, fill=colortext)

	# ----- Texte pourcentage budget -----
	percent = round(kgeq /5.5*100) #calcul de la part du budget carbone (5,5kgCO2eq/jour/personne), arrondi à l'unité
	if percent >=10 and percent<100 :
		xp, yp = 338, 168
	elif percent < 10 :
		xp, yp = 358, 168
	else :
		xp, yp = 310, 168
	font2 = ImageFont.truetype("./static/font/Lato-Regular.ttf", size=58)
	draw.text((xp, yp), str(percent), font=font2,  fill=colortext)

	# ----- Texte equivalent km voiture -----
	km = round(kgeq/0.259) #calcul de l'équivalent en km en voiture (donnée de l'Ademe, voiture essence moyenne), arrondi à l'unité
	if km>= 10 :
		xkm, ykm = 818, 328
	else :
		xkm, ykm = 838, 328
	font3 = ImageFont.truetype("./static/font/Lato-Regular.ttf", size=48)
	draw.text((xkm, ykm), str(km), font=font3, fill=colortext)
	return logo,color

def create_logo_file(inputimage, outputimage, kgCO2eq) :
	logo, color = create_logo(inputimage, kgCO2eq)
	logo.save(outputimage, "png")
	return color

def afficher_logo(inputimage, outputimage, plat, kgCO2eq, nbre_pts, logo_a_completer) :
	## ------- Fond de l'affiche (logo CROUS, bandeau, texte) -------
	im0 = Image.open(inputimage) 
	draw = ImageDraw.Draw(im0)
	## ------- Textes nom du plat et nombre de points -------
	colortext = (0, 0, 0, 255)
	font = ImageFont.truetype("./static/font/GillBI.ttf", size=300)
	platcut = textwrap.wrap(plat, width=20)
	text_width, text_height = draw.textsize(plat, font)
	page_width, page_height = im0.size
	current_h, pad = 1300, 65
	for line in platcut:
		w, h = draw.textsize(line, font=font)
		position = ((page_width-w)/2, current_h)
		draw.text(position, line, colortext, font=font)
		current_h += h + pad

	current_h+= pad
	if float(nbre_pts) > 0 :
		pts = str(nbre_pts)+' pts'
		pts_width, pts_height = draw.textsize(pts, font=font)
		position_pts = ((page_width-pts_width)/2, current_h)
		font2 = ImageFont.truetype("./static/font/GillBI.ttf", size=300)
		draw.text(position_pts, pts, font=font2, fill=colortext)
		current_h+=pts_height + pad

	## ------- Logo -------
	logo = create_logo(logo_a_completer, kgCO2eq)
	lw, lh = logo.size
	marge = 150
	sizelogo = (page_width-marge,int(lh*(page_width-marge)/lw))
	biglogo=logo.resize(sizelogo, Image.ANTIALIAS)
	im0.paste(biglogo, (int(marge/2),current_h))
	# Pour convertir un png en pdf il faut d'abord convertir l'image RGBA en RGB
	affichergb = Image.new('RGB', im0.size, (255, 255, 255))  # white background
	affichergb.paste(im0, mask=im0.split()[3])
	affichergb.save(outputimage, "pdf")
	return affichergb

