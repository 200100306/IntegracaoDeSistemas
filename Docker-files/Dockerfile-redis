#Imagem oficial do Redis
FROM redis:latest

# Define o diretório de trabalho
WORKDIR /usr/local/etc/redis

# Copia o ficheiro de configuração personalizado (opcional)
#COPY redis.conf .

# Expondo a porta padrão do Redis
EXPOSE 6379

# Comando para iniciar o Redis com a configuração personalizada
CMD [ "redis-server" ] 
#CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]