# Migration and Docker management script for movie-reviews-recomm-api (PowerShell version)

param(
    [Parameter(Position=0)]
    [string]$Command,
    
    [Parameter(Position=1)]
    [string]$Description
)

function Show-Help {
    Write-Host "Movie Reviews API Migration Script (PowerShell)" -ForegroundColor Green
    Write-Host ""
    Write-Host "Usage: .\migrate.ps1 [command] [options]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Commands:" -ForegroundColor Cyan
    Write-Host "  generate `"description`"  - Generate a new migration file"
    Write-Host "  apply                   - Apply pending migrations"
    Write-Host "  restart                 - Restart backend container (applies migrations via start.sh)"
    Write-Host "  rebuild                 - Rebuild and restart all containers (for code changes)"
    Write-Host "  status                  - Show migration status and history"
    Write-Host "  full-migrate `"desc`"     - Generate and apply migration in one step"
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Yellow
    Write-Host "  .\migrate.ps1 generate `"add genres table`""
    Write-Host "  .\migrate.ps1 apply"
    Write-Host "  .\migrate.ps1 restart"
    Write-Host "  .\migrate.ps1 rebuild"
    Write-Host "  .\migrate.ps1 full-migrate `"add genres table`""
}

switch ($Command) {
    "generate" {
        if ([string]::IsNullOrEmpty($Description)) {
            Write-Host "Usage: .\migrate.ps1 generate `"description of changes`"" -ForegroundColor Red
            Write-Host "Example: .\migrate.ps1 generate `"add genres table`"" -ForegroundColor Red
            exit 1
        }
        Write-Host "Generating migration: $Description" -ForegroundColor Green
        docker-compose exec backend alembic revision --autogenerate -m $Description
    }
    
    "apply" {
        Write-Host "Applying migrations..." -ForegroundColor Green
        docker-compose exec backend alembic upgrade head
    }
    
    "restart" {
        Write-Host "Restarting backend container..." -ForegroundColor Green
        docker-compose restart backend
    }
    
    "rebuild" {
        Write-Host "Rebuilding and starting containers..." -ForegroundColor Green
        docker-compose up --build -d
    }
    
    "status" {
        Write-Host "Checking migration status..." -ForegroundColor Green
        docker-compose exec backend alembic current
        Write-Host "Available migrations:" -ForegroundColor Green
        docker-compose exec backend alembic history
    }
    
    "full-migrate" {
        if ([string]::IsNullOrEmpty($Description)) {
            Write-Host "Usage: .\migrate.ps1 full-migrate `"description of changes`"" -ForegroundColor Red
            Write-Host "Example: .\migrate.ps1 full-migrate `"add genres table`"" -ForegroundColor Red
            exit 1
        }
        Write-Host "Generating and applying migration: $Description" -ForegroundColor Green
        docker-compose exec backend alembic revision --autogenerate -m $Description
        docker-compose exec backend alembic upgrade head
    }
    
    default {
        Show-Help
    }
} 