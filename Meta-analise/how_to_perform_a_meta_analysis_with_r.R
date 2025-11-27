# Adaptação de How to perform a meta-analysis with R: a practical tutorial  
# doi: 10.1136/ebmental-2019-300117  

# Instalando os Packages
install.packages(c("meta", "metasens"))

# Carregando Bibliotecas
library(meta)
library(metasens)

data = read.csv("Cochrane.csv")

# Add nova variável: miss
data$miss = ifelse((data$drop.h + data$drop.p) == 0,
                  "Without missing data", "With missing data")

head(data)
str(data)

# Meta-análise de efeito fixo versus efeito aleatório (Realizei uma breve mudança no método de cáculo do tau, para comparação com Python)

m.publ = metabin(resp.h, resp.h + fail.h, resp.p, resp.p + fail.p,
                 data = data, studlab = paste0(authoryear),
                 label.e = "Haloperidol", label.c = "Placebo", #method.tau = "DL",
                 label.left = "Favours placebo", label.right = "Favours haloperidol")
summary(m.publ)

# Criando Forest plot simples

forest(m.publ, sortvar = authoryear, prediction = TRUE,
       file = "figure2.pdf", width = 10)

# Impacto dos dados ausentes

m.publ.sub = update(m.publ, subgroup = miss, print.subgroup.name = FALSE)
m.publ.sub

# Criando Forest plot subgrupos

forest(m.publ.sub, sortvar = authoryear,
       xlim = c(0.1, 100), at = c(0.1, 0.3, 1, 3, 10, 30, 100),
       test.subgroup.common = FALSE,
       label.test.subgroup.random = "Test for subgroup differences:",
       file = "figure3.pdf", width = 10)

#Imputando dados e criando gráfico

# Impute as no events (ICA-0) - default
mmiss.0 = metamiss(m.publ, drop.h, drop.p)
# Impute as events (ICA-1)
mmiss.1 = metamiss(m.publ, drop.h, drop.p, method = "1")
# Observed risk in control group (ICA-pc)
mmiss.pc = metamiss(m.publ, drop.h, drop.p, method = "pc")
# Observed risk in experimental group (ICA-pe)
mmiss.pe = metamiss(m.publ, drop.h, drop.p, method = "pe")
# Observed group-specific risks (ICA-p)
mmiss.p = metamiss(m.publ, drop.h, drop.p, method = "p")
# Best-case scenario (ICA-b)
mmiss.b = metamiss(m.publ, drop.h, drop.p, method = "b", small.values = "bad")
# Worst-case scenario (ICA-w)
mmiss.w = metamiss(m.publ, drop.h, drop.p, method = "w", small.values = "bad")
# Gamble-Hollis method
mmiss.gh = metamiss(m.publ, drop.h, drop.p, method = "GH")
# IMOR.e = 2 and IMOR.c = 2 (same as available case analysis)
mmiss.imor2 = metamiss(m.publ, drop.h, drop.p, method = "IMOR", IMOR.e = 2)
# IMOR.e = 0.5 and IMOR.c = 0.5
mmiss.imor0.5 = metamiss(m.publ, drop.h, drop.p, method = "IMOR", IMOR.e = 0.5)

meths = c("Available case analysis (ACA)",
          "Impute no events (ICA-0)", "Impute events (ICA-1)",
          "Observed risk in control group (ICA-pc)",
          "Observed risk in experimental group (ICA-pe)",
          "Observed group-specific risks (ICA-p)",
          "Best-case scenario (ICA-b)", "Worst-case scenario (ICA-w)",
          "Gamble-Hollis analysis",
          "IMOR.e = 2, IMOR.c = 2", "IMOR.e = 0.5, IMOR.c = 0.5")

# Use inverse-variance method for pooling (which is used for imputation methods)
m.publ.iv = update(m.publ, method = "Inverse")

# Combine results (random effects)
mbr = metabind(m.publ.iv,
               mmiss.0, mmiss.1,
               mmiss.pc, mmiss.pe, mmiss.p,
               mmiss.b, mmiss.w, mmiss.gh,
               mmiss.imor2, mmiss.imor0.5,
               name = meths, pooled = "random")

forest(
  mbr, xlim = c(0.5, 4),
  leftcols = c("studlab", "I2", "tau2", "Q", "pval.Q"),
  leftlab  = c("Meta-Analysis Method", "I2", "Tau2", "Q", "P-value"),
  type = "diamond",
  digits.addcols = c(4, 2, 2, 2),
  just.addcols = "right",
  file = "figure4.pdf",
  width = 10
)


# Criando o funnel plot

funnel(m.publ)

# Teste de Harbord's score para assimetria de funnel plot

metabias(m.publ, method.bias = "score")

# Método de "Aparar e preencher"

tf.publ = trimfill(m.publ)

summary(tf.publ)

funnel(tf.publ)

# Análise de limite em meta-análise

l1.publ = limitmeta(m.publ)
l1.publ

# Criando figura completa

pdf("figure5.pdf", width = 10, height = 10)
#
par(mfrow = c(2, 2), pty = "s",
    oma = c(0, 0, 0, 0), mar = c(4.1, 3.1, 2.1, 1.1))
#
funnel(m.publ, xlim = c(0.05, 50), axes = FALSE)
axis(1, at = c(0.1, 0.2, 0.5, 1, 2, 5, 10, 50))
axis(2, at = c(0, 0.5, 1, 1.5))
box()
title(main = "Panel A: Funnel plot", adj = 0)
#
funnel(m.publ, xlim = c(0.05, 50), axes = FALSE,
       contour.levels = c(0.9, 0.95, 0.99),
       col.contour = c("darkgray", "gray", "lightgray"))
legend("topright",
       c("p < 1%", "1% < p < 5%", "5% < p < 10%", "p > 10%"),
       fill = c("lightgray", "gray", "darkgray", "white"),
       border = "white", bg = "white")
axis(1, at = c(0.1, 0.2, 0.5, 1, 2, 5, 10, 50))
axis(2, at = c(0, 0.5, 1, 1.5))
box()
title(main = "Panel B: Contour-enhanced funnel plot", adj = 0)
#
funnel(tf.publ, xlim = c(0.05, 50), axes = FALSE)
axis(1, at = c(0.1, 0.2, 0.5, 1, 2, 5, 10, 50))
axis(2, at = c(0, 0.5, 1, 1.5))
box()
title(main = "Panel C: Trim-and-fill method", adj = 0)
#
funnel(l1.publ, xlim = c(0.05, 50), axes = FALSE,
       col.line = 8, lwd.line = 3)
axis(1, at = c(0.1, 0.2, 0.5, 1, 2, 5, 10, 50))
axis(2, at = c(0, 0.5, 1, 1.5))
box()
title(main = "Panel D: Limit meta-analysis", adj = 0)
#
dev.off()

