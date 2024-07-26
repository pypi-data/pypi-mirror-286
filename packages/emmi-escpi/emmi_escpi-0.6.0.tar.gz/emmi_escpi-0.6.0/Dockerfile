FROM python:latest

ARG ESCPI_SRC=/escpi_src
ARG ESCPI_FROM_PIP=yes

RUN useradd -u 9999 cthulhu && mkdir /home/cthulhu && chown cthulhu /home/cthulhu

RUN if [ -d "$ESCPI_SRC" ]; then \
        echo "Installing from local directory: $ESCPI_SRC" ;\
        pip install "$ESCPI_SRC"[test,all] ;\
    elif [ "$ESCPI_FROM_PIP" = "yes" ]; then \
        echo "Installing from pip" ;\
        pip install emmi_escpi[test,all] ;\
    else \
        echo "\n  ***\n  *** Source not found at \$ESCPI_SRC ($ESCPI_SRC) -- failing build now. \n  ***\n" ;\
        /bin/false ;\
    fi

USER cthulhu

# ESCPI cannot stand alone -- there is no entry point.
# You'd typically want to build your own images, based
# on this one.
#ENTRYPOINT oszitrace-ioc
