# Backup and Recovery Procedures for AI-Native Book

## Overview
This document outlines the backup and recovery procedures for the AI-Native Book with Docusaurus application, covering content, user data, and system configurations.

## Backup Strategy

### 1. Content Backup (MDX Files)
**Location**: `website/docs/`
**Frequency**: Daily
**Method**: Git repository with automated pushes

```bash
# Automated backup script for content
#!/bin/bash
cd /path/to/your/repository
git add .
git commit -m "Automated content backup $(date)"
git push origin main
```

### 2. Database Backup (PostgreSQL)
**Frequency**: Daily at 2 AM
**Retention**: 30 days of daily backups, 12 months of monthly backups

```bash
# Database backup script
#!/bin/bash
BACKUP_DIR="/backups/database"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="ai_book_db"
DB_USER="ai_book_user"

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Perform backup
pg_dump -U $DB_USER -h localhost $DB_NAME > $BACKUP_DIR/ai_book_$DATE.sql

# Compress backup
gzip $BACKUP_DIR/ai_book_$DATE.sql

# Remove backups older than 30 days
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete
```

### 3. Vector Database Backup (Qdrant)
**Frequency**: Daily at 3 AM
**Method**: Qdrant snapshots

```bash
# Qdrant backup script
#!/bin/bash
BACKUP_DIR="/backups/qdrant"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Create Qdrant snapshot
curl -X POST "http://localhost:6333/snapshots"

# Get list of snapshots
curl -X GET "http://localhost:6333/snapshots" > $BACKUP_DIR/snapshots_$DATE.json

# Download snapshots if available
# (Implementation depends on your Qdrant setup and storage)
```

### 4. Configuration Backup
**Location**: `.env`, `docusaurus.config.js`, `docker-compose.yml`, etc.
**Frequency**: On change or weekly
**Method**: Git repository

## Recovery Procedures

### 1. Content Recovery
**Scenario**: MDX files corrupted or deleted

**Steps**:
1. Navigate to the website directory:
   ```bash
   cd /path/to/your/website
   ```
2. Restore from the latest Git commit:
   ```bash
   git log --oneline  # Find the last good commit
   git reset --hard <commit-hash>  # Restore to that commit
   ```
3. Verify content is accessible:
   ```bash
   npm run build  # Test build
   ```

### 2. Database Recovery
**Scenario**: PostgreSQL database corruption or data loss

**Steps**:
1. Stop the application:
   ```bash
   docker-compose down
   ```
2. Connect to PostgreSQL:
   ```bash
   psql -U ai_book_user -d ai_book_db
   ```
3. If database needs to be recreated:
   ```sql
   DROP DATABASE ai_book_db;
   CREATE DATABASE ai_book_db OWNER ai_book_user;
   \q
   ```
4. Restore from backup:
   ```bash
   gunzip -c /backups/database/ai_book_<date>.sql.gz | psql -U ai_book_user -d ai_book_db
   ```
5. Restart the application:
   ```bash
   docker-compose up -d
   ```

### 3. Vector Database Recovery
**Scenario**: Qdrant vector database issues

**Steps**:
1. Stop the Qdrant service:
   ```bash
   docker-compose stop qdrant
   ```
2. Restore Qdrant data from snapshot:
   ```bash
   # Remove corrupted data
   rm -rf /path/to/qdrant/storage/*

   # Restore from backup
   # (Specific implementation depends on how snapshots are stored)
   ```
3. Restart Qdrant:
   ```bash
   docker-compose start qdrant
   ```

### 4. Complete System Recovery
**Scenario**: Complete system failure

**Steps**:
1. Provision new infrastructure
2. Install Docker and Docker Compose
3. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```
4. Restore environment configuration:
   ```bash
   cp /secure/location/.env.example .env
   # Update with secure values
   ```
5. Restore database backup (as per database recovery steps)
6. Restore content (as per content recovery steps)
7. Start the application:
   ```bash
   docker-compose up -d
   ```

## Backup Verification

### 1. Automated Verification
Schedule weekly verification of backups:

```bash
# Verification script
#!/bin/bash
BACKUP_DIR="/backups/database"
LATEST_BACKUP=$(ls -t $BACKUP_DIR/*.sql.gz | head -n1)

# Check if backup is less than 24 hours old
if [ $(find $LATEST_BACKUP -mmin -1440 | wc -l) -eq 1 ]; then
    echo "✓ Backup is recent"
else
    echo "✗ Backup is outdated"
    exit 1
fi

# Check backup file size (should be > 1KB)
if [ $(gzip -l $LATEST_BACKUP | awk 'NR==2 {print $2}') -gt 1024 ]; then
    echo "✓ Backup has reasonable size"
else
    echo "✗ Backup file is too small"
    exit 1
fi

echo "✓ Backup verification passed"
```

### 2. Manual Verification
- Monthly: Perform a test recovery to a staging environment
- Quarterly: Validate that all backup procedures work as expected

## Disaster Recovery Plan

### 1. Communication Plan
- Notify stakeholders of the incident
- Provide estimated recovery time
- Update on recovery progress

### 2. Recovery Priority
1. **Critical**: User authentication, core content access
2. **High**: Search functionality, AI assistant
3. **Medium**: Analytics, user preferences
4. **Low**: Non-essential features

### 3. Rollback Procedures
If recovery causes new issues:
1. Document the problems
2. Revert to the previous working state
3. Investigate the cause
4. Plan a corrected recovery approach

## Security Considerations

### 1. Encrypted Backups
- Database backups should be encrypted
- Use strong encryption keys
- Store keys separately from backups

### 2. Access Control
- Limit access to backup systems
- Use role-based permissions
- Audit all backup and recovery activities

### 3. Off-site Storage
- Store copies of critical backups off-site
- Use cloud storage for geographic redundancy
- Test off-site restore procedures regularly

## Monitoring and Alerting

### 1. Backup Success/Failure Alerts
- Alert on backup failures
- Alert on verification failures
- Alert on backup storage capacity issues

### 2. Recovery Testing
- Schedule regular recovery tests
- Document recovery times
- Update procedures based on test results

## Maintenance

### 1. Regular Updates
- Update backup scripts as needed
- Adjust retention policies based on requirements
- Review and update this document quarterly

### 2. Team Training
- Train team members on backup procedures
- Conduct regular disaster recovery drills
- Maintain updated contact information for recovery team

## Contact Information

**Primary Recovery Contact**: [To be filled by administrator]
**Secondary Recovery Contact**: [To be filled by administrator]
**Cloud Provider Support**: [To be filled based on provider]
**Database Administrator**: [To be filled by administrator]

---

**Document Version**: 1.0
**Last Updated**: [Current Date]
**Next Review**: [Date + 3 months]