# services/analytics_service.py
import time
import math
from typing import Dict, List, Any
from services.database import MiniDBClient
from services.auth_service import AuthService

class AnalyticsService:
    """Analytics and dashboard data service"""
    
    def __init__(self, auth_service: AuthService):
        self.db = MiniDBClient()
        self.auth_service = auth_service
    
    def get_dashboard_stats(self, user_id: int) -> Dict[str, Any]:
        """Get comprehensive dashboard statistics"""
        user = self.auth_service.get_user_by_id(user_id)
        if not user:
            raise Exception("User not found")
        
        # Get all products
        all_products = self.db.select('products')
        all_users = self.db.select('users', "is_active = 1")
        
        # Calculate product statistics
        total_products = len(all_products)
        total_value = 0
        total_revenue = 0
        low_stock_count = 0
        product_categories = {}
        
        for row in all_products:
            try:
                price = float(row[3]) if row[3] else 0
                stock = int(row[5]) if row[5] else 0
                category = row[4] or "Uncategorized"
                
                # Total value (price * stock)
                total_value += price * stock
                
                # Total revenue (sum of prices)
                total_revenue += price
                
                # Low stock count
                if stock < 10:
                    low_stock_count += 1
                
                # Category distribution
                product_categories[category] = product_categories.get(category, 0) + 1
            except (ValueError, TypeError):
                continue
        
        # Calculate growth rate
        growth_rate = self._calculate_growth_rate(all_products)
        
        # Get average price
        average_price = total_revenue / total_products if total_products > 0 else 0
        
        # Get recent products (last 5 created)
        recent_products = self._get_recent_products(all_products, 5)
        
        # Get recent users (last 5 registered)
        recent_users = self._get_recent_users(all_users, 5)
        
        # Get activity timeline
        activity_log = self._get_activity_log(user_id, recent_products, recent_users)
        
        # Get top categories
        top_categories = sorted(product_categories.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Get monthly trend
        monthly_trend = self._get_monthly_trend(all_products)
        
        # Calculate user statistics
        total_users = len(all_users)
        user_roles = {}
        for row in all_users:
            try:
                role_id = row[4]
                role = self.auth_service.get_role_by_id(role_id)
                role_name = role['name'] if role else "Unknown"
                user_roles[role_name] = user_roles.get(role_name, 0) + 1
            except:
                continue
        
        return {
            "summary": {
                "total_products": total_products,
                "total_users": total_users,
                "total_value": total_value,
                "total_revenue": total_revenue,
                "growth_rate": growth_rate,
                "low_stock_count": low_stock_count,
                "average_price": average_price,
                "product_count_by_category": product_categories,
                "user_count_by_role": user_roles
            },
            "recent": {
                "products": recent_products,
                "users": recent_users
            },
            "insights": {
                "top_categories": top_categories,
                "monthly_trend": monthly_trend,
                "stock_status": {
                    "low_stock": low_stock_count,
                    "in_stock": total_products - low_stock_count
                }
            },
            "activity": activity_log,
            "user_info": {
                "username": user['username'],
                "role": user['role_name'],
                "permissions": user['permissions']
            }
        }
    
    def _calculate_growth_rate(self, products: List) -> float:
        """Calculate monthly growth rate based on product creation dates"""
        current_month = time.strftime('%Y-%m')
        last_month = self._get_previous_month()
        
        current_month_count = 0
        last_month_count = 0
        
        for row in products:
            try:
                created_at = row[7]  # created_at column
                if not created_at:
                    continue
                
                # Parse date (assuming format: YYYY-MM-DD HH:MM:SS)
                month_key = created_at[:7]
                
                if month_key == current_month:
                    current_month_count += 1
                elif month_key == last_month:
                    last_month_count += 1
            except:
                continue
        
        if last_month_count == 0:
            return 100.0 if current_month_count > 0 else 0.0
        
        return ((current_month_count - last_month_count) / last_month_count) * 100
    
    def _get_previous_month(self) -> str:
        """Get previous month in YYYY-MM format"""
        import datetime
        today = datetime.datetime.now()
        first = today.replace(day=1)
        last_month = first - datetime.timedelta(days=1)
        return last_month.strftime('%Y-%m')
    
    def _get_recent_products(self, products: List, limit: int = 5) -> List[Dict]:
        """Get most recently created products"""
        # Sort by created_at (assuming index 7)
        sorted_products = sorted(
            products,
            key=lambda x: x[7] if x[7] else '',
            reverse=True
        )[:limit]
        
        recent = []
        for row in sorted_products:
            try:
                recent.append({
                    'id': row[0],
                    'name': row[1],
                    'description': row[2] or '',
                    'price': float(row[3]) if row[3] else 0,
                    'category': row[4] or 'Uncategorized',
                    'stock': int(row[5]) if row[5] else 0,
                    'created_by': row[6],
                    'created_at': row[7] or '',
                    'status': 'Low Stock' if (int(row[5]) if row[5] else 0) < 10 else 'In Stock'
                })
            except:
                continue
        
        return recent
    
    def _get_recent_users(self, users: List, limit: int = 5) -> List[Dict]:
        """Get most recently registered users"""
        # Sort by created_at (assuming index 5)
        sorted_users = sorted(
            users,
            key=lambda x: x[5] if x[5] else '',
            reverse=True
        )[:limit]
        
        recent = []
        for row in sorted_users:
            try:
                user_id = row[0]
                role = self.auth_service.get_role_by_id(row[4])
                
                recent.append({
                    'id': user_id,
                    'username': row[1],
                    'email': row[2] or '',
                    'role_name': role['name'] if role else 'Unknown',
                    'created_at': row[5] or '',
                    'is_active': bool(row[6])
                })
            except:
                continue
        
        return recent
    
    def _get_activity_log(self, user_id: int, recent_products: List[Dict], recent_users: List[Dict]) -> List[Dict]:
        """Generate activity log based on recent events"""
        activities = []
        
        # Add product activities
        for product in recent_products[:2]:  # Last 2 products
            activities.append({
                'type': 'product_added',
                'message': f'New product "{product["name"]}" added',
                'time': self._format_time_ago(product.get('created_at', '')),
                'icon': 'Package',
                'color': 'blue'
            })
        
        # Add user activities
        for user in recent_users[:2]:  # Last 2 users
            activities.append({
                'type': 'user_joined',
                'message': f'New user "{user["username"]}" registered',
                'time': self._format_time_ago(user.get('created_at', '')),
                'icon': 'User',
                'color': 'green'
            })
        
        # Add system activity
        activities.append({
            'type': 'system_update',
            'message': 'Dashboard refreshed with latest data',
            'time': 'Just now',
            'icon': 'Activity',
            'color': 'purple'
        })
        
        return activities
    
    def _format_time_ago(self, timestamp: str) -> str:
        """Format timestamp as time ago string"""
        if not timestamp:
            return "Recently"
        
        try:
            import datetime
            from dateutil import parser
            
            # Parse the timestamp
            dt = parser.parse(timestamp)
            now = datetime.datetime.now()
            diff = now - dt
            
            if diff.days > 30:
                months = diff.days // 30
                return f"{months} month{'s' if months > 1 else ''} ago"
            elif diff.days > 0:
                return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
            elif diff.seconds > 3600:
                hours = diff.seconds // 3600
                return f"{hours} hour{'s' if hours > 1 else ''} ago"
            elif diff.seconds > 60:
                minutes = diff.seconds // 60
                return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
            else:
                return "Just now"
        except:
            return "Recently"
    
    def _get_monthly_trend(self, products: List) -> List[Dict]:
        """Get product creation trend for the last 6 months"""
        import datetime
        from collections import defaultdict
        
        monthly_data = defaultdict(int)
        today = datetime.datetime.now()
        
        # Initialize last 6 months
        for i in range(6):
            month = (today.month - i - 1) % 12 + 1
            year = today.year - ((today.month - i - 1) // 12)
            key = f"{year}-{month:02d}"
            monthly_data[key] = 0
        
        # Count products per month
        for row in products:
            try:
                created_at = row[7]
                if not created_at:
                    continue
                
                # Extract year-month
                month_key = created_at[:7]
                if month_key in monthly_data:
                    monthly_data[month_key] += 1
            except:
                continue
        
        # Convert to list of dicts
        trend = []
        for month_key in sorted(monthly_data.keys()):
            year, month = map(int, month_key.split('-'))
            month_name = datetime.datetime(year, month, 1).strftime('%b %Y')
            trend.append({
                'month': month_name,
                'count': monthly_data[month_key]
            })
        
        return trend