<p align="center">
  <h1 align="center">🛒 Swift Cart</h1>
  <p align="center">
    A full-featured multi-vendor e-commerce marketplace built with Django
    <br />
    <a href="#features"><strong>Explore Features »</strong></a>
    <br />
    <br />
    <a href="#installation">Installation</a>
    ·
    <a href="#screenshots">Screenshots</a>
    ·
    <a href="#tech-stack">Tech Stack</a>
  </p>
</p>

---

## 📖 About

**Swift Cart** is a multi-vendor e-commerce platform that seamlessly connects vendors and customers. Vendors can set up their own storefronts, list products, and manage inventory, while customers can browse, search, and purchase products from multiple sellers — all in one place.

---

## ✨ Features

### For Vendors
- **Product Listing & Management** — Upload products with multiple images, set pricing, manage stock levels, and categorize items
- **Vendor Profiles** — Dedicated business profiles with profile pictures, business descriptions, and city information
- **Analytics & Insights** — Track sales and manage orders with status tracking (Pending → Shipped → Delivered)
- **Order Management** — View and fulfill customer orders

### For Customers
- **Advanced Search** — Full-text product search powered by Whoosh/Haystack
- **Browse by Category** — Filter and explore products across categories
- **Shopping Cart** — Add items, adjust quantities, and proceed to checkout
- **Wishlist** — Save products for later
- **Order Tracking** — Track order status from purchase to delivery
- **Vendor Reviews** — Rate and review vendors with a 5-star rating system

### General
- **Role-Based Authentication** — Separate signup flows for vendors and customers with email-based login
- **Featured Products** — Curated recommendations, trending items, and top sellers on the homepage
- **Responsive Design** — Built with Bootstrap 5 for a seamless experience on all devices

---

## 📸 Screenshots

### Homepage
The landing page features a hero section, featured product carousel, and an about section.

![Homepage](static/images/readme/Screenshot%202026-02-22%20044624.png)

### Role-Based Signup
Users choose to register as a **Vendor** or **Customer**, each with tailored onboarding.

![Signup Page](static/images/readme/Screenshot%202026-02-22%20044643.png)

### Product Browsing
Browse products from multiple vendors, filter by category, and search with ease.

![Browse Products](static/images/readme/Screenshot%202026-02-22%20044951.png)

### Services & Features
Detailed breakdown of vendor and customer features.

![Services Page](static/images/readme/Screenshot%202026-02-22%20045030.png)

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Django 5.1 |
| **Frontend** | Django Templates, Bootstrap 5 |
| **Database** | SQLite (dev) / PostgreSQL (prod-ready) |
| **Search** | Whoosh + Django Haystack |
| **Authentication** | Django Allauth |
| **Task Queue** | Celery + AMQP |
| **Image Processing** | Pillow, Easy Thumbnails, Django Image Cropping |

---

## 📁 Project Structure

```
swift-cart/
├── swift_cart/          # Main project settings & URL configuration
├── services/            # Core app — Products, Categories, Reviews, Featured Items
├── users/               # User management — Custom User, Vendor & Customer Profiles
├── checkouts/           # Cart, Orders, Wishlist & Checkout flow
├── templates/           # Shared base templates
├── static/              # Static assets (CSS, JS, images)
├── media/               # User-uploaded files (product images, profile photos)
├── requirements.txt     # Python dependencies
└── manage.py            # Django management script
```

---

## 🚀 Installation

### Prerequisites
- Python 3.10+
- pip

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Nashiol/swift-cart.git
   cd swift-cart
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser** (for admin access)
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. Open your browser and navigate to `http://127.0.0.1:8000/`

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

