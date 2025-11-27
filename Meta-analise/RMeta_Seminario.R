# Instalando os Packages
install.packages(c("meta", "metasens"))

# Carregando Bibliotecas
library(meta)
library(metasens)

# Importando Dados
data = read.csv("Cochrane.csv")
total.h = data$resp.h + data$fail.h
total.p = data$resp.p + data$fail.p

# Forest Plot
m.publ_t = metabin(resp.h, total.h, resp.p, total.p,
                   data = data,
                   studlab = paste0(authoryear))

summary(m.publ_t)

forest(m.publ_t,
       file = "figure_new.pdf",
       width = 10)

# Funnel Plot
funnel(m.publ_t)

# Teste de Egger e Harbord
metabias(m.publ_t, method.bias = "linreg") #Egger
metabias(m.publ_t, method.bias = "score") #Harbord

