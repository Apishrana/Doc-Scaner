
if [[ ! -f backend/.env ]] || \
   ! grep -q "^FIREBASE_CREDENTIALS=" backend/.env || \
   ! grep -q "^DEBUG=" backend/.env || \
   ! grep -q "^SUPABASE_URL=" backend/.env || \
   ! grep -q "^SUPABASE_KEY=" backend/.env || \
   ! grep -q "^BACKEND_HOST=" backend/.env || \
   ! grep -q "^BACKEND_PORT=" backend/.env; then
cat > backend/.env <<EOF
# Supabase
SUPABASE_URL=Use Your Url from Supabase project
SUPABASE_KEY=Use Your Key from Supabase project

# Backend
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# Auth
SECRET_KEY=`openssl rand -hex 32`
ALGORITHM=HS256
TOKEN_EXPIRATION_TIME_MINUTS=525600

# Firebase
FIREBASE_CREDENTIALS=Use Your firebase.json

DEBUG=True
EOF
    echo "backend/.env created/updated"
fi

if [[ ! -f frontend/.env ]] || \
   ! grep -q "^EXPO_PUBLIC_BACKEND_URL=" App/.env ; then
cat > frontend/.env <<EOF
EXPO_PUBLIC_BACKEND_URL=http://0.0.0.0:8000
EOF
    echo "App/.env created/updated"
fi


cd backend;
uv sync;

cd ../;

cd frontend;
npm i;

