#!/bin/bash

# Migration and Docker management script for movie-reviews-recomm-api

case "$1" in
    "generate")
        # Generate a new migration
        if [ -z "$2" ]; then
            echo "Usage: ./migrate.sh generate \"description of changes\""
            echo "Example: ./migrate.sh generate \"add genres table\""
            exit 1
        fi
        echo "Generating migration: $2"
        docker-compose exec backend alembic revision --autogenerate -m "$2"
        ;;
    
    "apply")
        # Apply migrations
        echo "Applying migrations..."
        docker-compose exec backend alembic upgrade head
        ;;
    
    "restart")
        # Restart backend to apply migrations via start.sh
        echo "Restarting backend container..."
        docker-compose restart backend
        ;;
    
    "rebuild")
        # Rebuild and restart everything (for code changes)
        echo "Rebuilding and starting containers..."
        docker-compose up --build -d
        ;;
    
    "status")
        # Check migration status
        echo "Checking migration status..."
        docker-compose exec backend alembic current
        echo "Available migrations:"
        docker-compose exec backend alembic history
        ;;
    
    "full-migrate")
        # Generate and apply migration in one command
        if [ -z "$2" ]; then
            echo "Usage: ./migrate.sh full-migrate \"description of changes\""
            echo "Example: ./migrate.sh full-migrate \"add genres table\""
            exit 1
        fi
        echo "Generating and applying migration: $2"
        docker-compose exec backend alembic revision --autogenerate -m "$2"
        docker-compose exec backend alembic upgrade head
        ;;
    
    *)
        echo "Movie Reviews API Migration Script"
        echo ""
        echo "Usage: ./migrate.sh [command] [options]"
        echo ""
        echo "Commands:"
        echo "  generate \"description\"  - Generate a new migration file"
        echo "  apply                   - Apply pending migrations"
        echo "  restart                 - Restart backend container (applies migrations via start.sh)"
        echo "  rebuild                 - Rebuild and restart all containers (for code changes)"
        echo "  status                  - Show migration status and history"
        echo "  full-migrate \"desc\"     - Generate and apply migration in one step"
        echo ""
        echo "Examples:"
        echo "  ./migrate.sh generate \"add genres table\""
        echo "  ./migrate.sh apply"
        echo "  ./migrate.sh restart"
        echo "  ./migrate.sh rebuild"
        echo "  ./migrate.sh full-migrate \"add genres table\""
        ;;
esac 