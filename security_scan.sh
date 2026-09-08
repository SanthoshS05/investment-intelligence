#!/usr/bin/env bash

# ============================================================
# Investment Intelligence - Pre-Push Security Scanner
#
# Scans the repository for:
#   - credentials
#   - API keys
#   - passwords
#   - tokens
#   - private keys
#   - emails
#   - phone numbers
#   - IP addresses
#   - personal paths
#   - portfolio information
#   - secret-looking configuration
#
# IMPORTANT:
# This scanner MASKS matching values in output.
# ============================================================

set +e

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

cd "$ROOT" || exit 1

echo
echo "============================================================"
echo " INVESTMENT INTELLIGENCE - SECURITY SCAN"
echo "============================================================"
echo
echo "Root:"
echo "  $ROOT"
echo
echo "Scanning working tree..."
echo


# ============================================================
# CONFIGURATION
# ============================================================

EXCLUDE_DIRS=(
    ".git"
    ".venv"
    "venv"
    "__pycache__"
    ".pytest_cache"
    "node_modules"
    ".mypy_cache"
    ".idea"
    ".vscode"
    "reports"
)

EXCLUDE_ARGS=()

for dir in "${EXCLUDE_DIRS[@]}"; do
    EXCLUDE_ARGS+=(
        "--exclude-dir=$dir"
    )
done


# ============================================================
# COUNTERS
# ============================================================

TOTAL_FINDINGS=0


# ============================================================
# HELPER
# ============================================================

run_scan() {

    local title="$1"
    local pattern="$2"

    echo
    echo "------------------------------------------------------------"
    echo " $title"
    echo "------------------------------------------------------------"

    # grep:
    # -R recursive
    # -n line number
    # -I ignore binary files
    # -E extended regex
    #
    # We intentionally don't use -i globally.
    # Individual patterns handle case sensitivity.

    RESULTS=$(grep \
        -RniIE \
        "${EXCLUDE_ARGS[@]}" \
        --exclude="*.pyc" \
        --exclude="*.png" \
        --exclude="*.jpg" \
        --exclude="*.jpeg" \
        --exclude="*.gif" \
        --exclude="*.webp" \
        --exclude="*.zip" \
        --exclude="*.tar" \
        --exclude="*.gz" \
        --exclude="*.sqlite" \
        --exclude="*.db" \
        "$pattern" \
        . 2>/dev/null)

    if [ -z "$RESULTS" ]; then
        echo "  ✓ No findings"
        return
    fi

    COUNT=$(printf '%s\n' "$RESULTS" | wc -l)

    TOTAL_FINDINGS=$((TOTAL_FINDINGS + COUNT))

    # --------------------------------------------------------
    # MASK likely sensitive values before printing.
    # --------------------------------------------------------

    printf '%s\n' "$RESULTS" |
        sed -E \
            -e 's/([A-Za-z0-9_]*PASSWORD[A-Za-z0-9_]*[[:space:]]*=[[:space:]]*)[^[:space:]]+/\1********/Ig' \
            -e 's/([A-Za-z0-9_]*API[_-]?KEY[A-Za-z0-9_]*[[:space:]]*=[[:space:]]*)[^[:space:]]+/\1********/Ig' \
            -e 's/([A-Za-z0-9_]*TOKEN[A-Za-z0-9_]*[[:space:]]*=[[:space:]]*)[^[:space:]]+/\1********/Ig' \
            -e 's/([A-Za-z0-9_]*SECRET[A-Za-z0-9_]*[[:space:]]*=[[:space:]]*)[^[:space:]]+/\1********/Ig' \
            -e 's/([A-Za-z0-9_]*PASSWORD[A-Za-z0-9_]*[[:space:]]*:[[:space:]]*)[^,} ]+/\1********/Ig' \
            -e 's/(https?:\/\/[^:\/[:space:]]+):[^@\/[:space:]]+@/\1:********@/g'

    echo
}


# ============================================================
# 1. EMAIL ADDRESSES
# ============================================================

run_scan \
    "EMAIL ADDRESSES" \
    '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'


# ============================================================
# 2. API KEYS / SECRET VARIABLES
# ============================================================

run_scan \
    "API KEYS / SECRET VARIABLES" \
    '(API[_-]?KEY|APP[_-]?PASSWORD|PASSWORD|SECRET|ACCESS[_-]?KEY|AUTH[_-]?TOKEN|BEARER[_-]?TOKEN|CLIENT[_-]?SECRET|PRIVATE[_-]?KEY)[[:space:]]*[:=]'


# ============================================================
# 3. GOOGLE / GMAIL CREDENTIALS
# ============================================================

run_scan \
    "GOOGLE / GMAIL CREDENTIALS" \
    '(gmail|google|smtp\.gmail\.com|EMAIL_USER|EMAIL_APP_PASSWORD|EMAIL_TO)'


# ============================================================
# 4. FRED / MARKET API CREDENTIALS
# ============================================================

run_scan \
    "MARKET / FRED API CREDENTIALS" \
    '(FRED_API_KEY|MARKET_API_KEY|NEWS_API_KEY|ALPHA[_-]?VANTAGE|FINNHUB|POLYGON[_-]?API|TWELVE[_-]?DATA)'


# ============================================================
# 5. COMMON CLOUD CREDENTIALS
# ============================================================

run_scan \
    "CLOUD CREDENTIALS" \
    '(AWS_ACCESS_KEY_ID|AWS_SECRET_ACCESS_KEY|GOOGLE_APPLICATION_CREDENTIALS|AZURE_CLIENT_SECRET|AZURE_CLIENT_ID|AZURE_TENANT_ID|AKIA[0-9A-Z]{16})'


# ============================================================
# 6. PRIVATE KEYS
# ============================================================

run_scan \
    "PRIVATE KEYS" \
    '-----BEGIN ([A-Z0-9 ]+)?PRIVATE KEY-----'


# ============================================================
# 7. JWT TOKENS
# ============================================================

run_scan \
    "JWT TOKENS" \
    'eyJ[A-Za-z0-9_-]{5,}\.[A-Za-z0-9_-]{5,}\.[A-Za-z0-9_-]{5,}'


# ============================================================
# 8. BEARER TOKENS
# ============================================================

run_scan \
    "BEARER TOKENS" \
    'Bearer[[:space:]]+[A-Za-z0-9._~+\/=-]{15,}'


# ============================================================
# 9. BASIC AUTH URLs
# ============================================================

run_scan \
    "CREDENTIALS INSIDE URLS" \
    'https?://[^[:space:]]+:[^[:space:]@]+@'


# ============================================================
# 10. PHONE NUMBERS
# ============================================================

run_scan \
    "POSSIBLE PHONE NUMBERS" \
    '(\+91[- .]?[6-9][0-9]{9}|[6-9][0-9]{9})'


# ============================================================
# 11. PRIVATE / INTERNAL IP ADDRESSES
# ============================================================

run_scan \
    "PRIVATE IP ADDRESSES" \
    '(^|[^0-9])(10\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}|192\.168\.[0-9]{1,3}\.[0-9]{1,3}|172\.(1[6-9]|2[0-9]|3[0-1])\.[0-9]{1,3}\.[0-9]{1,3})'


# ============================================================
# 12. LOCAL USER PATHS
# ============================================================

run_scan \
    "LOCAL USER / MACHINE PATHS" \
    '(/home/[A-Za-z0-9._-]+/|/Users/[A-Za-z0-9._-]+/|C:\\\\Users\\\\[A-Za-z0-9._-]+)'


# ============================================================
# 13. ABSOLUTE DESKTOP PATHS
# ============================================================

run_scan \
    "ABSOLUTE DESKTOP PATHS" \
    '(/home/|/Users/|C:\\\\Users\\\\|Desktop/|Documents/)'


# ============================================================
# 14. PORTFOLIO / SIP DATA
# ============================================================

run_scan \
    "PORTFOLIO / SIP INFORMATION" \
    '(PORTFOLIO|monthly_sip|SIP|XIRR|UTI Nifty|HDFC Mid Cap|Nippon Taiwan|KVB RD)'


# ============================================================
# 15. PERSONAL INFORMATION KEYWORDS
# ============================================================

run_scan \
    "PERSONAL INFORMATION KEYWORDS" \
    '(full[_-]?name|first[_-]?name|last[_-]?name|phone|mobile|address|home[_-]?address|date[_-]?of[_-]?birth|dob|personal[_-]?email)'


# ============================================================
# 16. SECRET-LIKE ASSIGNMENTS
# ============================================================

run_scan \
    "SECRET-LIKE ASSIGNMENTS" \
    '([A-Za-z0-9_]*(password|passwd|secret|token|apikey|api_key|access_key)[A-Za-z0-9_]*[[:space:]]*=[[:space:]]*["'\'']?[^"'\''][^"'\'']*["'\'']?)'


# ============================================================
# 17. ENVIRONMENT FILES
# ============================================================

echo
echo "------------------------------------------------------------"
echo " ENVIRONMENT / SECRET FILES"
echo "------------------------------------------------------------"

ENV_FILES=$(find . \
    -type f \
    \( \
        -name ".env" \
        -o -name ".env.*" \
        -o -name "*.pem" \
        -o -name "*.key" \
        -o -name "*credentials*" \
        -o -name "*secret*" \
    \) \
    ! -path "./.git/*" \
    ! -path "./.venv/*" \
    2>/dev/null)

if [ -z "$ENV_FILES" ]; then
    echo "  ✓ No obvious secret files found"
else
    echo "$ENV_FILES"
    COUNT=$(printf '%s\n' "$ENV_FILES" | wc -l)
    TOTAL_FINDINGS=$((TOTAL_FINDINGS + COUNT))
fi


# ============================================================
# 18. GIT TRACKED SECRET FILES
# ============================================================

echo
echo "------------------------------------------------------------"
echo " GIT-TRACKED SECRET FILES"
echo "------------------------------------------------------------"

TRACKED_SECRET_FILES=$(git ls-files 2>/dev/null |
    grep -Ei \
        '(^|/)(\.env|\.env\..*|.*\.pem|.*\.key|.*credentials.*|.*secret.*)$')

if [ -z "$TRACKED_SECRET_FILES" ]; then
    echo "  ✓ No obvious secret files tracked by Git"
else
    echo "$TRACKED_SECRET_FILES"
    COUNT=$(printf '%s\n' "$TRACKED_SECRET_FILES" | wc -l)
    TOTAL_FINDINGS=$((TOTAL_FINDINGS + COUNT))
fi


# ============================================================
# 19. GITIGNORE CHECK
# ============================================================

echo
echo "------------------------------------------------------------"
echo " .GITIGNORE SECURITY CHECK"
echo "------------------------------------------------------------"

if [ ! -f ".gitignore" ]; then

    echo "  ❌ .gitignore does not exist"

else

    REQUIRED_PATTERNS=(
        ".env"
        ".venv/"
        "__pycache__/"
        "*.pyc"
        "reports/"
    )

    for pattern in "${REQUIRED_PATTERNS[@]}"; do

        if grep -Fxq "$pattern" ".gitignore"; then
            echo "  ✓ $pattern"
        else
            echo "  ❌ MISSING: $pattern"
            TOTAL_FINDINGS=$((TOTAL_FINDINGS + 1))
        fi

    done

fi


# ============================================================
# 20. GIT HISTORY SCAN
# ============================================================

echo
echo "------------------------------------------------------------"
echo " GIT HISTORY - SECRET PATTERNS"
echo "------------------------------------------------------------"

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then

    HISTORY_RESULTS=$(git log -p --all 2>/dev/null |
        grep -Ei \
            '(APP_PASSWORD|API_KEY|SECRET|PASSWORD|PRIVATE_KEY|BEGIN .*PRIVATE KEY|Bearer[[:space:]]+eyJ)' |
        head -100)

    if [ -z "$HISTORY_RESULTS" ]; then
        echo "  ✓ No obvious secret patterns found in Git history"
    else
        echo "  ⚠️ Potential historical findings:"
        echo
        echo "$HISTORY_RESULTS" |
            sed -E \
                -e 's/(PASSWORD|APP_PASSWORD|API_KEY|SECRET|PRIVATE_KEY)[^=]*=[^[:space:]]+/\1=********/Ig' |
            head -100
    fi

else

    echo "  Git repository not detected."

fi


# ============================================================
# SUMMARY
# ============================================================

echo
echo "============================================================"
echo " SCAN COMPLETE"
echo "============================================================"
echo

if [ "$TOTAL_FINDINGS" -eq 0 ]; then

    echo "  ✅ No obvious privacy/security findings detected."
    echo
    echo "  This does NOT guarantee that the repository is safe."
    echo "  Review the project manually before publishing."

else

    echo "  ⚠️ Findings detected: $TOTAL_FINDINGS"
    echo
    echo "  DO NOT push to GitHub yet."
    echo
    echo "  Review each finding above."
    echo "  Some findings may be legitimate code/configuration."
    echo "  Others may require removal or relocation to GitHub Secrets."

fi

echo
echo "============================================================"