---
name: drupaltools-developer-setup
description: Configure a developer's local machine for Drupal development. Use this skill when setting up a new development machine, configuring PHP/Composer/DDEV, installing Drupal CLI tools, or optimizing IDE and terminal for Drupal work.
---

# Drupal Developer Machine Setup

Configure a local development machine for Drupal work.

## Scope

**This skill covers:**
- Machine-level software installation
- CLI tools (Drush, Drupalorg CLI, Composer)
- PHP configuration and version management
- Docker/DDEV setup
- IDE configuration (PhpStorm, VS Code)
- Terminal utilities (OhMyZsh, Tmux)
- Code quality tools (PHPCS, PHPStan, CaptainHook)

**For project-level guidance**, use `drupaltools-checklist-development`.

## Process

### 1. Detect Current State

Check what's installed:
```bash
php --version
composer --version
docker --version
drush --version
```

### 2. Core Installation

**PHP:**
```bash
# Ubuntu/DDEV-compatible
sudo apt install php8.2-cli php8.2-mysql php8.2-xml php8.2-mbstring php8.2-curl
```

**Composer:**
```bash
curl -sS https://getcomposer.org/installer | php
sudo mv composer.phar /usr/local/bin/composer
```

**Drush Launcher:**
```bash
curl -fsSL https://github.com/drush-ops/drush-launcher/releases/latest/download/drush.phar -o /usr/local/bin/drush
chmod +x /usr/local/bin/drush
```

### 3. Docker/DDEV

**DDEV with extensions:**
```bash
docker pull drud/ddev-php8.2 || true
ddev config global --instrumentation-opt-in=false
ddev start
```

### 4. IDE Setup

**PhpStorm essential plugins:**
- PHP Inspections (EA Extended)
- Deep Associative Array Completion
- DrupalStorm
- .ignore

### 5. Code Quality Tools

```bash
composer global require drupal/coder squizlabs/php_codesniffer phpstan/phpstan
```

## Reference

| Component | Package | Purpose |
|----------|---------|---------|
| PHP | php8.2-* | Core Drupal requirements |
| Drush | drush-launcher | CLI for Drupal |
| Composer | global | Dependency management |
| DDEV | docker-based | Local environment |
| PHPCS | drupal/coder | Code standards |
| PHPStan | phpstan/phpstan | Static analysis |
