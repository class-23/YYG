#!/bin/bash
# ============================================================
# SSL 证书生成脚本（开发环境）
# 生产环境请使用 Let's Encrypt 或正式 CA 证书
# ============================================================
set -e

DOMAIN=${1:-api.yuanyuangao.com}
SSL_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "生成 $DOMAIN 的自签名证书（仅用于开发）..."

# 生成 2048 位 DH 参数
if [ ! -f "$SSL_DIR/dhparam.pem" ]; then
    echo "生成 dhparam.pem（首次约需 2 分钟）..."
    openssl dhparam -out "$SSL_DIR/dhparam.pem" 2048
fi

# 生成私钥
openssl genrsa -out "$SSL_DIR/$DOMAIN.key" 2048

# 生成自签名证书（365 天）
openssl req -new -x509 -key "$SSL_DIR/$DOMAIN.key" \
    -out "$SSL_DIR/$DOMAIN.crt" -days 365 \
    -subj "/C=CN/ST=Beijing/L=Beijing/O=MomEnglish/OU=IT/CN=$DOMAIN"

echo "✅ 证书生成完成:"
echo "  证书: $SSL_DIR/$DOMAIN.crt"
echo "  私钥: $SSL_DIR/$DOMAIN.key"
echo ""
echo "生产环境请使用 Let's Encrypt:"
echo "  certbot certonly --webroot -w /var/www/certbot -d $DOMAIN"
