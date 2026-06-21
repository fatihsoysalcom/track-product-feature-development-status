import datetime

class Feature:
    """Represents a product feature with its development status."""
    STATUS_BACKLOG = "BACKLOG"
    STATUS_IN_PROGRESS = "IN_PROGRESS"
    STATUS_BLOCKED = "BLOCKED"
    STATUS_TESTING = "TESTING"
    STATUS_DONE = "DONE"

    def __init__(self, name, description="", assigned_to="Unassigned"):
        self.name = name
        self.description = description
        self.assigned_to = assigned_to
        self.status = self.STATUS_BACKLOG # Initial status
        self.created_at = datetime.date.today()
        self.last_updated_at = datetime.date.today()
        self.history = [(self.created_at, self.status, "Feature created")]

    def update_status(self, new_status, notes=""):
        """Updates the feature's status and logs the change."""
        if new_status not in [self.STATUS_BACKLOG, self.STATUS_IN_PROGRESS,
                              self.STATUS_BLOCKED, self.STATUS_TESTING,
                              self.STATUS_DONE]:
            print(f"Warning: Invalid status '{new_status}' for feature '{self.name}'. Status not updated.")
            return

        if self.status != new_status:
            self.status = new_status
            self.last_updated_at = datetime.date.today()
            self.history.append((self.last_updated_at, self.status, notes))
            print(f"Feature '{self.name}' status updated to '{new_status}'.")
        else:
            print(f"Feature '{self.name}' status is already '{new_status}'.")

    def __str__(self):
        return (f"Feature: {self.name}\n"
                f"  Status: {self.status}\n"
                f"  Assigned: {self.assigned_to}\n"
                f"  Created: {self.created_at}\n"
                f"  Last Updated: {self.last_updated_at}\n"
                f"  Description: {self.description[:50]}...") # Truncate description for display

class ProductDevelopmentTracker:
    """Manages a collection of features for a product."""
    def __init__(self):
        self.features = {} # Dictionary to store features by name

    def add_feature(self, feature):
        """Adds a new feature to the tracker."""
        if feature.name in self.features:
            print(f"Error: Feature '{feature.name}' already exists.")
            return False
        self.features[feature.name] = feature
        print(f"Feature '{feature.name}' added to tracker.")
        return True

    def get_feature(self, name):
        """Retrieves a feature by its name."""
        return self.features.get(name)

    def list_features_by_status(self, status):
        """Lists all features currently in a specific status."""
        print(f"\n--- Features in '{status}' status ---")
        found = False
        for feature in self.features.values():
            if feature.status == status:
                print(f"- {feature.name} (Assigned to: {feature.assigned_to}, Last Updated: {feature.last_updated_at})")
                found = True
        if not found:
            print(f"No features found in '{status}' status.")
        return found

    def identify_stalled_features(self, days_stalled=7):
        """Identifies features that haven't been updated recently and are not DONE."""
        today = datetime.date.today()
        stalled = []
        print(f"\n--- Identifying potentially stalled features (not updated in {days_stalled} days) ---")
        for feature in self.features.values():
            if feature.status != Feature.STATUS_DONE:
                days_since_update = (today - feature.last_updated_at).days
                if days_since_update >= days_stalled:
                    stalled.append(feature)
                    print(f"- '{feature.name}' (Status: {feature.status}, Last updated {days_since_update} days ago)")
        if not stalled:
            print("No stalled features identified.")
        return stalled

# --- Main demonstration ---
if __name__ == "__main__":
    print("--- Simulating a 4-Month Product Development Cycle ---")

    tracker = ProductDevelopmentTracker()

    # Month 1: Initial feature definition
    print("\n--- Month 1: Initial Feature Definition ---")
    feature1 = Feature("User Authentication", "Secure login and registration for users.", "Alice")
    feature2 = Feature("Product Listing Page", "Display available products with search/filter.", "Bob")
    feature3 = Feature("Shopping Cart", "Allow users to add/remove items to a cart.", "Charlie")

    tracker.add_feature(feature1)
    tracker.add_feature(feature2)
    tracker.add_feature(feature3)

    # Simulate some initial progress
    feature1.update_status(Feature.STATUS_IN_PROGRESS, "Started backend integration.")
    feature2.update_status(Feature.STATUS_IN_PROGRESS, "Designing UI/UX for product cards.")

    # Month 2: Development continues, some features get blocked
    print("\n--- Month 2: Development Progress & Challenges ---")
    # Simulate time passing for demonstration purposes (e.g., 30 days later)
    # In a real scenario, `datetime.date.today()` would naturally advance.
    # For this demo, we'll manually set `last_updated_at` for some features to simulate time.
    feature1.last_updated_at = datetime.date.today() - datetime.timedelta(days=20) # Simulate it being worked on earlier
    feature2.last_updated_at = datetime.date.today() - datetime.timedelta(days=15)
    feature3.last_updated_at = datetime.date.today() - datetime.timedelta(days=5) # This one is newer

    feature1.update_status(Feature.STATUS_BLOCKED, "Waiting for API endpoint from another team.") # Illustrates a common development hurdle
    feature3.update_status(Feature.STATUS_IN_PROGRESS, "Started implementing add-to-cart logic.")

    # Identify features that might be stuck, demonstrating problem identification in development.
    tracker.identify_stalled_features(days_stalled=10) # Check for features not updated in 10 days

    # Month 3: Unblocking and new features
    print("\n--- Month 3: Resolving Blocks & New Features ---")
    # Simulate unblocking feature1
    feature1.update_status(Feature.STATUS_IN_PROGRESS, "API endpoint is ready, resuming work.")
    feature1.last_updated_at = datetime.date.today() # Reset last updated after unblock

    feature4 = Feature("Payment Gateway Integration", "Integrate with Stripe for secure payments.", "Alice")
    tracker.add_feature(feature4)
    feature4.update_status(Feature.STATUS_IN_PROGRESS, "Researching Stripe API.")

    # Month 4: Nearing launch, testing and completion
    print("\n--- Month 4: Nearing Launch - Testing & Completion ---")
    feature2.update_status(Feature.STATUS_TESTING, "Product listing UI/UX ready for review.")
    feature3.update_status(Feature.STATUS_TESTING, "Shopping cart functionality complete, testing required.")
    feature1.update_status(Feature.STATUS_TESTING, "Authentication flow tested, minor bugs found.")

    # Simulate final fixes and completion
    feature1.update_status(Feature.STATUS_DONE, "All authentication bugs resolved.")
    feature2.update_status(Feature.STATUS_DONE, "Product listing approved and deployed.")
    feature3.update_status(Feature.STATUS_DONE, "Shopping cart passed all tests.")

    # Final status overview
    print("\n--- Final Status Overview Before Launch ---")
    tracker.list_features_by_status(Feature.STATUS_DONE)
    tracker.list_features_by_status(Feature.STATUS_TESTING)
    tracker.list_features_by_status(Feature.STATUS_IN_PROGRESS)
    tracker.list_features_by_status(Feature.STATUS_BLOCKED)
    tracker.list_features_by_status(Feature.STATUS_BACKLOG)

    # Check for any remaining stalled features before final launch.
    tracker.identify_stalled_features(days_stalled=5) # Shorter period before launch
