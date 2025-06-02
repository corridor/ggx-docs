---
title: Install using Docker
---

Corridor provides production-ready Dockerfile templates along with the installation bundle to bootstrap a docker-based installation of the platform.

As docker configurations frequently vary based on various organizations - Please reach out to us for instructions on docker-based installs

Various components of the platform are addressed as follows in this setup:

<!-- Bullet points within markdown style tables turned out in a messy format. Going bare metal here. -->
<table>
  <thead>
    <tr>
      <th>Component</th>
      <th>Implementation Options</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>File Management</td>
      <td>Mounted to host/persistent volume</td>
    </tr>
    <tr>
      <td>Metadata Database</td>
      <td>Configurable as an independent service / Can integrate with an existing service</td>
    </tr>
    <tr>
      <td>Messaging Queue</td>
      <td>Configurable as an independent service / Can integrate with an existing service</td>
    </tr>
    <tr>
      <td>SSL Certificates</td>
      <td>
        <ul>
            <li>Mounted from host/persistent volume in read-only mode</li>
            <li>Copied to image during docker build stage</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>Platform Configurations</td>
      <td>
        <ul>
            <li>Mounted from host/persistent volume in read-only mode</li>
            <li>Via environment variables during deployment</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>Spark</td>
      <td>Configurable as an independent service / Can integrate with an existing service</td>
    </tr>
    <tr>
      <td>Jupyterhub</td>
      <td>Configurable as an independent service / Can integrate with an existing service</td>
    </tr>
  </tbody>
</table>

## System: Minimum Requirements

<!-- TODO: Update docker compose version? -->

- Docker Engine: v20.10+
- (Optional) Docker compose
