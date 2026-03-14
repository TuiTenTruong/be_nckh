// ============================================================================
// DATABASE SCHEMA - Ung dung Nhan dien Nguyen lieu & Goi y Cong thuc AI
// ============================================================================
// Tong hop tu phan tich 7 man hinh UI va mock data hien tai
// Database: PostgreSQL (Supabase)
// Tong cong: 13 bang chinh + 1 bang KV co san
// ============================================================================

// ============================================================================
// BANG 1: users - Thong tin nguoi dung
// ============================================================================
// Lien quan: Profile page (avatar, ten, ngay tham gia, thong ke)
// ============================================================================
export interface UsersTable {
  id: string;                    // UUID, PRIMARY KEY (tu Supabase Auth)
  email: string;                 // VARCHAR(255), UNIQUE, NOT NULL
  name: string;                  // VARCHAR(100), NOT NULL
  avatar_url: string | null;     // TEXT, nullable - URL anh dai dien
  member_since: string;          // TIMESTAMP, DEFAULT now()
  total_cooked: number;          // INTEGER, DEFAULT 0 - So mon da nau
  total_scanned: number;         // INTEGER, DEFAULT 0 - So lan quet
  created_at: string;            // TIMESTAMP, DEFAULT now()
  updated_at: string;            // TIMESTAMP, DEFAULT now()
}
// SQL:
// CREATE TABLE users (
//   id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
//   email VARCHAR(255) UNIQUE NOT NULL,
//   name VARCHAR(100) NOT NULL,
//   avatar_url TEXT,
//   member_since TIMESTAMP WITH TIME ZONE DEFAULT now(),
//   total_cooked INTEGER DEFAULT 0,
//   total_scanned INTEGER DEFAULT 0,
//   created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
//   updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
// );

// ============================================================================
// BANG 2: ingredient_categories - Danh muc nguyen lieu
// ============================================================================
// Lien quan: mockData.ts -> category: 'protein' | 'vegetable' | 'spice' | 'grain'
// ============================================================================
export interface IngredientCategoriesTable {
  id: string;                    // UUID, PRIMARY KEY
  slug: string;                  // VARCHAR(50), UNIQUE - vd: 'protein', 'vegetable'
  name: string;                  // VARCHAR(100), NOT NULL - vd: 'Chat dam', 'Rau cu'
  icon: string | null;           // VARCHAR(10), nullable - Emoji icon
  sort_order: number;            // INTEGER, DEFAULT 0
}
// SQL:
// CREATE TABLE ingredient_categories (
//   id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
//   slug VARCHAR(50) UNIQUE NOT NULL,
//   name VARCHAR(100) NOT NULL,
//   icon VARCHAR(10),
//   sort_order INTEGER DEFAULT 0
// );
// INSERT INTO ingredient_categories (slug, name, icon, sort_order) VALUES
//   ('protein', 'Chat dam', '🥩', 1),
//   ('vegetable', 'Rau cu', '🥬', 2),
//   ('spice', 'Gia vi', '🧄', 3),
//   ('grain', 'Ngu coc', '🌾', 4),
//   ('seafood', 'Hai san', '🦐', 5),
//   ('dairy', 'Sua & Trung', '🥚', 6),
//   ('sauce', 'Nuoc cham & Sot', '🫙', 7),
//   ('other', 'Khac', '🥘', 8);

// ============================================================================
// BANG 3: ingredients - Nguyen lieu tong (master list)
// ============================================================================
// Lien quan: mockData.ts -> popularIngredients[], ScanIngredients, Ingredients page
// ============================================================================
export interface IngredientsTable {
  id: string;                    // UUID, PRIMARY KEY
  name: string;                  // VARCHAR(100), UNIQUE, NOT NULL
  icon: string;                  // VARCHAR(10), NOT NULL - Emoji
  category_id: string;           // UUID, FK -> ingredient_categories.id
  image_url: string | null;      // TEXT, nullable - Anh nguyen lieu (cho AI scan)
  is_popular: boolean;           // BOOLEAN, DEFAULT false - Hien thi o trang chu
  aliases: string[] | null;      // TEXT[], nullable - Ten goi khac (cho AI nhan dien)
  created_at: string;            // TIMESTAMP, DEFAULT now()
}
// SQL:
// CREATE TABLE ingredients (
//   id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
//   name VARCHAR(100) UNIQUE NOT NULL,
//   icon VARCHAR(10) NOT NULL,
//   category_id UUID NOT NULL REFERENCES ingredient_categories(id),
//   image_url TEXT,
//   is_popular BOOLEAN DEFAULT false,
//   aliases TEXT[],
//   created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
// );
// CREATE INDEX idx_ingredients_category ON ingredients(category_id);
// CREATE INDEX idx_ingredients_popular ON ingredients(is_popular) WHERE is_popular = true;

// ============================================================================
// BANG 4: recipes - Cong thuc nau an
// ============================================================================
// Lien quan: mockData.ts -> recipes[], RecipeSuggestions, RecipeDetail page
// ============================================================================
export interface RecipesTable {
  id: string;                    // UUID, PRIMARY KEY
  name: string;                  // VARCHAR(200), NOT NULL
  description: string;           // TEXT, NOT NULL
  image_url: string;             // TEXT, NOT NULL - Anh mon an (Unsplash)
  cook_time_minutes: number;     // INTEGER, NOT NULL - Thoi gian nau (phut)
  cook_time_display: string;     // VARCHAR(50), NOT NULL - vd: '45 phut'
  difficulty: DifficultyLevel;   // VARCHAR(20), NOT NULL - 'De' | 'Trung binh' | 'Kho'
  servings: number;              // INTEGER, NOT NULL - So nguoi an
  cuisine_type: string | null;   // VARCHAR(50), nullable - vd: 'Viet Nam', 'Han Quoc'
  diet_tags: string[] | null;    // TEXT[], nullable - vd: ['chay', 'it dau mo']
  is_featured: boolean;          // BOOLEAN, DEFAULT false - Goi y hom nay
  total_favorites: number;       // INTEGER, DEFAULT 0
  total_views: number;           // INTEGER, DEFAULT 0
  created_at: string;            // TIMESTAMP, DEFAULT now()
  updated_at: string;            // TIMESTAMP, DEFAULT now()
}

export type DifficultyLevel = 'De' | 'Trung binh' | 'Kho';

// SQL:
// CREATE TABLE recipes (
//   id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
//   name VARCHAR(200) NOT NULL,
//   description TEXT NOT NULL,
//   image_url TEXT NOT NULL,
//   cook_time_minutes INTEGER NOT NULL,
//   cook_time_display VARCHAR(50) NOT NULL,
//   difficulty VARCHAR(20) NOT NULL CHECK (difficulty IN ('De', 'Trung binh', 'Kho')),
//   servings INTEGER NOT NULL DEFAULT 2,
//   cuisine_type VARCHAR(50),
//   diet_tags TEXT[],
//   is_featured BOOLEAN DEFAULT false,
//   total_favorites INTEGER DEFAULT 0,
//   total_views INTEGER DEFAULT 0,
//   created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
//   updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
// );
// CREATE INDEX idx_recipes_difficulty ON recipes(difficulty);
// CREATE INDEX idx_recipes_featured ON recipes(is_featured) WHERE is_featured = true;
// CREATE INDEX idx_recipes_cook_time ON recipes(cook_time_minutes);

// ============================================================================
// BANG 5: recipe_ingredients - Nguyen lieu cua cong thuc (N-N)
// ============================================================================
// Lien quan: mockData.ts -> RecipeIngredient[], RecipeDetail page (checklist)
// ============================================================================
export interface RecipeIngredientsTable {
  id: string;                    // UUID, PRIMARY KEY
  recipe_id: string;             // UUID, FK -> recipes.id, NOT NULL
  ingredient_id: string | null;  // UUID, FK -> ingredients.id, nullable (co the la nguyen lieu tu do)
  ingredient_name: string;       // VARCHAR(100), NOT NULL - Ten hien thi
  amount: string;                // VARCHAR(50), NOT NULL - vd: '500g', '2 cu'
  is_optional: boolean;          // BOOLEAN, DEFAULT false - Nguyen lieu tuy chon
  sort_order: number;            // INTEGER, DEFAULT 0
}
// SQL:
// CREATE TABLE recipe_ingredients (
//   id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
//   recipe_id UUID NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
//   ingredient_id UUID REFERENCES ingredients(id) ON DELETE SET NULL,
//   ingredient_name VARCHAR(100) NOT NULL,
//   amount VARCHAR(50) NOT NULL,
//   is_optional BOOLEAN DEFAULT false,
//   sort_order INTEGER DEFAULT 0
// );
// CREATE INDEX idx_recipe_ingredients_recipe ON recipe_ingredients(recipe_id);
// CREATE INDEX idx_recipe_ingredients_ingredient ON recipe_ingredients(ingredient_id);

// ============================================================================
// BANG 6: recipe_steps - Cac buoc nau an
// ============================================================================
// Lien quan: mockData.ts -> RecipeStep[], RecipeDetail page (step-by-step view)
// ============================================================================
export interface RecipeStepsTable {
  id: string;                    // UUID, PRIMARY KEY
  recipe_id: string;             // UUID, FK -> recipes.id, NOT NULL
  step_number: number;           // INTEGER, NOT NULL
  title: string | null;          // VARCHAR(200), nullable - Tieu de buoc
  description: string;           // TEXT, NOT NULL - Mo ta chi tiet
  image_url: string | null;      // TEXT, nullable - Anh minh hoa buoc
  duration_minutes: number | null; // INTEGER, nullable - Thoi gian uoc tinh buoc nay
  tip: string | null;            // TEXT, nullable - Meo nau an
}
// SQL:
// CREATE TABLE recipe_steps (
//   id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
//   recipe_id UUID NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
//   step_number INTEGER NOT NULL,
//   title VARCHAR(200),
//   description TEXT NOT NULL,
//   image_url TEXT,
//   duration_minutes INTEGER,
//   tip TEXT,
//   UNIQUE(recipe_id, step_number)
// );
// CREATE INDEX idx_recipe_steps_recipe ON recipe_steps(recipe_id);

// ============================================================================
// BANG 7: user_pantry - Tu nguyen lieu cua nguoi dung
// ============================================================================
// Lien quan: Ingredients page (grid card, them/xoa), ScanIngredients page
// ============================================================================
export interface UserPantryTable {
  id: string;                    // UUID, PRIMARY KEY
  user_id: string;               // UUID, FK -> users.id, NOT NULL
  ingredient_id: string;         // UUID, FK -> ingredients.id, NOT NULL
  quantity: string | null;        // VARCHAR(50), nullable - So luong (tuy chon)
  added_via: PantrySource;       // VARCHAR(20), NOT NULL - 'manual' | 'scan' | 'recipe'
  added_at: string;              // TIMESTAMP, DEFAULT now()
  expires_at: string | null;     // TIMESTAMP, nullable - Han su dung
}

export type PantrySource = 'manual' | 'scan' | 'recipe';

// SQL:
// CREATE TABLE user_pantry (
//   id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
//   user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
//   ingredient_id UUID NOT NULL REFERENCES ingredients(id) ON DELETE CASCADE,
//   quantity VARCHAR(50),
//   added_via VARCHAR(20) NOT NULL DEFAULT 'manual'
//     CHECK (added_via IN ('manual', 'scan', 'recipe')),
//   added_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
//   expires_at TIMESTAMP WITH TIME ZONE,
//   UNIQUE(user_id, ingredient_id)
// );
// CREATE INDEX idx_user_pantry_user ON user_pantry(user_id);

// ============================================================================
// BANG 8: user_favorites - Mon an yeu thich
// ============================================================================
// Lien quan: Profile page (tab Yeu thich), RecipeDetail (nut tim)
// ============================================================================
export interface UserFavoritesTable {
  id: string;                    // UUID, PRIMARY KEY
  user_id: string;               // UUID, FK -> users.id, NOT NULL
  recipe_id: string;             // UUID, FK -> recipes.id, NOT NULL
  created_at: string;            // TIMESTAMP, DEFAULT now()
}
// SQL:
// CREATE TABLE user_favorites (
//   id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
//   user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
//   recipe_id UUID NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
//   created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
//   UNIQUE(user_id, recipe_id)
// );
// CREATE INDEX idx_user_favorites_user ON user_favorites(user_id);

// ============================================================================
// BANG 9: user_history - Lich su xem/nau
// ============================================================================
// Lien quan: Profile page (tab Lich su, hien thi ngay xem)
// ============================================================================
export interface UserHistoryTable {
  id: string;                    // UUID, PRIMARY KEY
  user_id: string;               // UUID, FK -> users.id, NOT NULL
  recipe_id: string;             // UUID, FK -> recipes.id, NOT NULL
  action: HistoryAction;         // VARCHAR(20), NOT NULL - 'viewed' | 'cooked' | 'shared'
  created_at: string;            // TIMESTAMP, DEFAULT now()
}

export type HistoryAction = 'viewed' | 'cooked' | 'shared';

// SQL:
// CREATE TABLE user_history (
//   id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
//   user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
//   recipe_id UUID NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
//   action VARCHAR(20) NOT NULL DEFAULT 'viewed'
//     CHECK (action IN ('viewed', 'cooked', 'shared')),
//   created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
// );
// CREATE INDEX idx_user_history_user ON user_history(user_id);
// CREATE INDEX idx_user_history_created ON user_history(created_at DESC);

// ============================================================================
// BANG 10: user_diet_preferences - Tuy chon che do an
// ============================================================================
// Lien quan: Profile page (Che do an cua ban - 4 options)
// ============================================================================
export interface UserDietPreferencesTable {
  id: string;                    // UUID, PRIMARY KEY
  user_id: string;               // UUID, FK -> users.id, NOT NULL
  diet_type: DietType;           // VARCHAR(30), NOT NULL
  is_active: boolean;            // BOOLEAN, DEFAULT true
  created_at: string;            // TIMESTAMP, DEFAULT now()
}

export type DietType = 'normal' | 'vegetarian' | 'low_fat' | 'diet' | 'no_gluten' | 'no_lactose';

// SQL:
// CREATE TABLE user_diet_preferences (
//   id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
//   user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
//   diet_type VARCHAR(30) NOT NULL
//     CHECK (diet_type IN ('normal', 'vegetarian', 'low_fat', 'diet', 'no_gluten', 'no_lactose')),
//   is_active BOOLEAN DEFAULT true,
//   created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
//   UNIQUE(user_id, diet_type)
// );
// CREATE INDEX idx_user_diet_user ON user_diet_preferences(user_id);

// ============================================================================
// BANG 11: scan_sessions - Phien quet nguyen lieu
// ============================================================================
// Lien quan: ScanIngredients page (camera, nut quet, ket qua chip)
// ============================================================================
export interface ScanSessionsTable {
  id: string;                    // UUID, PRIMARY KEY
  user_id: string;               // UUID, FK -> users.id, NOT NULL
  image_url: string | null;      // TEXT, nullable - Anh chup tu camera
  scan_type: ScanType;           // VARCHAR(20), NOT NULL - 'camera' | 'upload'
  status: ScanStatus;            // VARCHAR(20), NOT NULL
  total_detected: number;        // INTEGER, DEFAULT 0
  created_at: string;            // TIMESTAMP, DEFAULT now()
}

export type ScanType = 'camera' | 'upload';
export type ScanStatus = 'processing' | 'completed' | 'failed';

// SQL:
// CREATE TABLE scan_sessions (
//   id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
//   user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
//   image_url TEXT,
//   scan_type VARCHAR(20) NOT NULL DEFAULT 'camera'
//     CHECK (scan_type IN ('camera', 'upload')),
//   status VARCHAR(20) NOT NULL DEFAULT 'processing'
//     CHECK (status IN ('processing', 'completed', 'failed')),
//   total_detected INTEGER DEFAULT 0,
//   created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
// );
// CREATE INDEX idx_scan_sessions_user ON scan_sessions(user_id);
// CREATE INDEX idx_scan_sessions_created ON scan_sessions(created_at DESC);

// ============================================================================
// BANG 12: scan_results - Ket qua nhan dien nguyen lieu
// ============================================================================
// Lien quan: ScanIngredients page (danh sach chip nguyen lieu phat hien)
// ============================================================================
export interface ScanResultsTable {
  id: string;                    // UUID, PRIMARY KEY
  scan_session_id: string;       // UUID, FK -> scan_sessions.id, NOT NULL
  ingredient_id: string | null;  // UUID, FK -> ingredients.id, nullable
  detected_name: string;         // VARCHAR(100), NOT NULL - Ten AI nhan dien
  confidence: number;            // DECIMAL(5,4), NOT NULL - Do chinh xac (0.0 - 1.0)
  is_confirmed: boolean;         // BOOLEAN, DEFAULT false - User xac nhan dung
  is_removed: boolean;           // BOOLEAN, DEFAULT false - User xoa bo
  bounding_box: object | null;   // JSONB, nullable - Vi tri trong anh {x, y, w, h}
}
// SQL:
// CREATE TABLE scan_results (
//   id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
//   scan_session_id UUID NOT NULL REFERENCES scan_sessions(id) ON DELETE CASCADE,
//   ingredient_id UUID REFERENCES ingredients(id) ON DELETE SET NULL,
//   detected_name VARCHAR(100) NOT NULL,
//   confidence DECIMAL(5,4) NOT NULL DEFAULT 0.0,
//   is_confirmed BOOLEAN DEFAULT false,
//   is_removed BOOLEAN DEFAULT false,
//   bounding_box JSONB
// );
// CREATE INDEX idx_scan_results_session ON scan_results(scan_session_id);

// ============================================================================
// BANG 13: chat_messages - Tin nhan chat AI
// ============================================================================
// Lien quan: ChatAI page (giao dien chat, goi y cau hoi, recipe cards)
// ============================================================================
export interface ChatMessagesTable {
  id: string;                    // UUID, PRIMARY KEY
  user_id: string;               // UUID, FK -> users.id, NOT NULL
  conversation_id: string;       // UUID, NOT NULL - Nhom cac tin nhan theo phien
  role: ChatRole;                // VARCHAR(10), NOT NULL - 'user' | 'ai'
  content: string;               // TEXT, NOT NULL - Noi dung tin nhan
  recipe_ids: string[] | null;   // UUID[], nullable - Cac recipe AI goi y kem
  metadata: object | null;       // JSONB, nullable - Du lieu bo sung (context, tokens, v.v.)
  created_at: string;            // TIMESTAMP, DEFAULT now()
}

export type ChatRole = 'user' | 'ai';

// SQL:
// CREATE TABLE chat_messages (
//   id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
//   user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
//   conversation_id UUID NOT NULL,
//   role VARCHAR(10) NOT NULL CHECK (role IN ('user', 'ai')),
//   content TEXT NOT NULL,
//   recipe_ids UUID[],
//   metadata JSONB,
//   created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
// );
// CREATE INDEX idx_chat_messages_user ON chat_messages(user_id);
// CREATE INDEX idx_chat_messages_conversation ON chat_messages(conversation_id);
// CREATE INDEX idx_chat_messages_created ON chat_messages(created_at DESC);


// ============================================================================
//
//  SO DO QUAN HE (ERD - Entity Relationship Diagram)
//
// ============================================================================
//
//  users (1) ──────< user_pantry (N) >────── ingredients (1)
//    │                                             │
//    │                                             │
//    ├──< user_favorites (N) >── recipes (1)       │
//    │                             │                │
//    ├──< user_history (N) >──────┘                │
//    │                             │                │
//    ├──< user_diet_preferences    ├──< recipe_ingredients (N) >── ingredients
//    │                             │
//    ├──< scan_sessions (N)        ├──< recipe_steps (N)
//    │       │
//    │       └──< scan_results (N) >── ingredients
//    │
//    └──< chat_messages (N)
//
//
//  ingredient_categories (1) ──< ingredients (N)
//
// ============================================================================


// ============================================================================
//
//  TONG HOP: 13 BANG - PHAN NHOM THEO CHUC NANG
//
// ============================================================================
//
//  NHOM 1 - NGUOI DUNG (4 bang)
//  ┌─────────────────────────────────────────────────────────────────────┐
//  │  users                    - Thong tin ca nhan                      │
//  │  user_pantry              - Tu nguyen lieu (them/xoa/quet)         │
//  │  user_favorites           - Danh sach yeu thich                   │
//  │  user_diet_preferences    - Che do an (chay, giam can, v.v.)      │
//  └─────────────────────────────────────────────────────────────────────┘
//
//  NHOM 2 - NGUYEN LIEU (2 bang)
//  ┌─────────────────────────────────────────────────────────────────────┐
//  │  ingredient_categories    - Danh muc: dam, rau, gia vi, ngu coc   │
//  │  ingredients              - Master list nguyen lieu + emoji + alias│
//  └─────────────────────────────────────────────────────────────────────┘
//
//  NHOM 3 - CONG THUC (3 bang)
//  ┌─────────────────────────────────────────────────────────────────────┐
//  │  recipes                  - Mon an (ten, anh, thoi gian, do kho)  │
//  │  recipe_ingredients       - Nguyen lieu cua mon (N-N)             │
//  │  recipe_steps             - Cac buoc nau (step-by-step)           │
//  └─────────────────────────────────────────────────────────────────────┘
//
//  NHOM 4 - QUET & AI (3 bang)
//  ┌─────────────────────────────────────────────────────────────────────┐
//  │  scan_sessions            - Phien quet (camera/upload)            │
//  │  scan_results             - Nguyen lieu AI nhan dien + confidence  │
//  │  chat_messages            - Lich su chat voi AI                   │
//  └─────────────────────────────────────────────────────────────────────┘
//
//  NHOM 5 - LICH SU (1 bang)
//  ┌─────────────────────────────────────────────────────────────────────┐
//  │  user_history             - Lich su xem/nau/chia se               │
//  └─────────────────────────────────────────────────────────────────────┘
//
// ============================================================================


// ============================================================================
//
//  MAPPING: MAN HINH UI  <-->  BANG CSDL
//
// ============================================================================
//
//  1. TRANG CHU (Home)
//     - Loi chao              -> users.name
//     - Tim kiem               -> recipes (full-text search), ingredients
//     - Nguyen lieu pho bien   -> ingredients (WHERE is_popular = true)
//     - Goi y hom nay          -> recipes (WHERE is_featured = true)
//                                 + recipe_ingredients JOIN user_pantry
//                                 => tinh so nguyen lieu thieu
//
//  2. QUET NGUYEN LIEU (ScanIngredients)
//     - Phien quet             -> scan_sessions (camera/upload)
//     - Ket qua nhan dien      -> scan_results (detected_name, confidence)
//     - Chip nguyen lieu        -> scan_results JOIN ingredients
//     - Xoa chip                -> scan_results.is_removed = true
//     - "Tim cong thuc"         -> chuyen sang RecipeSuggestions voi danh sach
//
//  3. DANH SACH NGUYEN LIEU (Ingredients)
//     - Grid nguyen lieu        -> user_pantry JOIN ingredients
//     - Them nguyen lieu        -> INSERT user_pantry (added_via = 'manual')
//     - Xoa nguyen lieu         -> DELETE user_pantry
//     - So luong hien thi       -> COUNT(user_pantry WHERE user_id = ?)
//
//  4. GOI Y CONG THUC (RecipeSuggestions)
//     - Danh sach cong thuc     -> recipes
//     - Bo loc (De/TB/Du NL)    -> recipes.difficulty, recipe_ingredients
//     - Thieu bao nhieu NL      -> recipe_ingredients LEFT JOIN user_pantry
//                                  => dem ingredient_id khong co trong pantry
//     - So nguoi, thoi gian     -> recipes.servings, recipes.cook_time_display
//
//  5. CHI TIET MON AN (RecipeDetail)
//     - Anh + thong tin         -> recipes.*
//     - Checklist nguyen lieu   -> recipe_ingredients LEFT JOIN user_pantry
//                                  => available = (ingredient_id IN user_pantry)
//     - Cac buoc nau            -> recipe_steps ORDER BY step_number
//     - Yeu thich (tim)         -> user_favorites (INSERT/DELETE)
//     - Chia se                 -> user_history (action = 'shared')
//     - Bat dau nau             -> user_history (action = 'cooked')
//
//  6. CHAT AI (ChatAI)
//     - Lich su tin nhan        -> chat_messages WHERE conversation_id = ?
//     - Gui tin nhan            -> INSERT chat_messages (role = 'user')
//     - AI tra loi              -> INSERT chat_messages (role = 'ai', recipe_ids)
//     - Recipe cards trong chat -> recipes WHERE id = ANY(recipe_ids)
//     - Goi y cau hoi           -> co the luu trong kv_store hoac hardcode
//
//  7. HO SO (Profile)
//     - Thong tin user          -> users.*
//     - Thong ke (12/45/28)     -> COUNT(user_favorites), users.total_cooked,
//                                  users.total_scanned
//     - Che do an               -> user_diet_preferences
//     - Tab Yeu thich           -> user_favorites JOIN recipes
//     - Tab Lich su             -> user_history JOIN recipes ORDER BY created_at
//     - Lich su quet            -> scan_sessions ORDER BY created_at
//
// ============================================================================


// ============================================================================
//  SUPABASE ROW LEVEL SECURITY (RLS) - Goi y
// ============================================================================
//
//  -- Moi user chi doc/ghi du lieu cua chinh minh
//  ALTER TABLE user_pantry ENABLE ROW LEVEL SECURITY;
//  CREATE POLICY "Users can manage own pantry"
//    ON user_pantry FOR ALL
//    USING (auth.uid() = user_id);
//
//  -- Tuong tu cho: user_favorites, user_history,
//  --               user_diet_preferences, scan_sessions, chat_messages
//
//  -- Recipes, ingredients, categories: public read
//  ALTER TABLE recipes ENABLE ROW LEVEL SECURITY;
//  CREATE POLICY "Anyone can read recipes"
//    ON recipes FOR SELECT USING (true);
//
// ============================================================================
