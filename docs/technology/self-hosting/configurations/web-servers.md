# Web Server Setup

## Nginx Configurations

This section described how to use nginx ([https://nginx.org/en/](https://nginx.org/en/)) as a web server. The Platform's server components can be made highly performant by using the lightweight Nginx as a reverse-proxy along with a WSGI server. Using nginx enabled the server to scale to a large number of users with ease.

To use Nginx, it needs to be installed in the system and the daemon should be running with the appropriate site configurations setup.

Here is an example nginx configuration:

```nginx
server {
  listen 80;
  server_name localhost 0.0.0.0;

  client_max_body_size 100m;
  gzip on;
  gzip_vary on;
  gzip_min_length 10240;
  gzip_proxied expired no-cache no-store private auth;
  gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/javascript application/xml application/json ;
  gzip_disable "MSIE [1-6]\.";

  location / {
    proxy_set_header   X-Real-IP        $remote_addr;
    proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
    proxy_set_header   X-Forwarded-Proto $scheme;
    proxy_set_header   Host             $http_host;

    proxy_pass http://localhost:5002;
    proxy_read_timeout 3600;
  }

  location /jupyter {
    proxy_set_header   X-Real-IP        $remote_addr;
    proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
    proxy_set_header   X-Forwarded-Proto $scheme;
    proxy_set_header   Host             $http_host;

    proxy_pass http://localhost:5003;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_read_timeout 86400;
  }
}
```

!!! note

    If the nginx is not listening on port 80 - but listens on another port, the `proxy_set_header` for `Host` may have to be modified to `proxy_set_header Host $http_host` to ensure the correct host information is passed.

!!! note "Note: Permission issues"

    In case of permission issues, ensure user permissions and SELinux is set up correctly.

!!! note "Note: Large file uploads"

    If large files are expected to be uploaded, there are two settings that need to be modified
    <br>
    &emsp; 1. add `proxy_request_buffering off`<br>
    &emsp; 2. add `client_max_body_size 0;`<br>
    to server directive which expects large file size payload.
    This will disable nginx from buffering the large payload files and optimize disk space consumption.

## Apache Configurations

To setup a secure connection, update the `/etc/httpd/sites-available/corridorapp.conf` file as below:

```httpd
<VirtualHost *:443>
    SSLEngine On
    SSLCertificateFile /certs/app.crt
    SSLCertificateKeyFile /certs/app.key
    SSLCertificateChainFile /certs/ca.crt
    ServerName www.corridorapp.com
    ServerAlias corridorapp
    ProxyPass / http://localhost:5002/
    ProxyPassReverse / http://localhost:5002/
    ErrorLog /var/www/corridorapp/log/error.log
    CustomLog /var/www/corridorapp/log/requests.log combined
</VirtualHost>
```

!!! note

    If the httpd is not listening on port 80 (443 for SSL) - but listens on another port, the corresponding port has to be added along with `VirtualHost` keyword and the `Listen` param's value has to be appropriately updated in `/etc/httpd/conf/httpd.conf` (`/etc/httpd/conf.d/ssl.conf` for SSL).

!!! note "Note: Permission issues"

    In case of permission issues, ensure user permissions and SELinux is set up correctly.
