"""
Automated Data Collection for Algorithm Comparison
Runs comparisons regularly and stores historical data
"""

import json
import time
import os
from datetime import datetime
from algorithm_comparison import ArbitrageComparison


class DataCollector:
    def __init__(self, data_directory: str = "comparison_data"):
        """
        Initialize data collector
        
        Args:
            data_directory: Directory to store comparison results
        """
        self.data_directory = data_directory
        self.collection_log = os.path.join(data_directory, "collection_log.txt")
        
        # Create data directory if it doesn't exist
        if not os.path.exists(data_directory):
            os.makedirs(data_directory)
            print(f"✅ Created data directory: {data_directory}")
        
        # Initialize log
        if not os.path.exists(self.collection_log):
            with open(self.collection_log, 'w') as f:
                f.write("=" * 80 + "\n")
                f.write("DATA COLLECTION LOG\n")
                f.write(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")
    
    def log_collection(self, message: str):
        """Log collection event"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}\n"
        
        print(log_entry.strip())
        
        with open(self.collection_log, 'a') as f:
            f.write(log_entry)
    
    def run_single_comparison(self) -> dict:
        """Run one comparison and save results"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(self.data_directory, f"comparison_{timestamp}.json")
        
        self.log_collection("Starting comparison...")
        
        try:
            # Run comparison
            comparison = ArbitrageComparison()
            
            if not comparison.fetch_market_data():
                self.log_collection("❌ Failed to fetch market data")
                return None
            
            comparison.run_bellman_ford()
            comparison.run_triangle_arbitrage()
            analysis = comparison.analyze_results()
            
            # Save to file
            with open(filename, 'w') as f:
                json.dump(analysis, f, indent=2)
            
            self.log_collection(f"✅ Saved results to {filename}")
            
            # Summary
            bf_count = analysis['bellman_ford']['count']
            tri_count = analysis['triangle']['count']
            winner = analysis['comparison']['overall_winner']
            
            self.log_collection(f"   Bellman-Ford: {bf_count} opportunities")
            self.log_collection(f"   Triangle: {tri_count} opportunities")
            self.log_collection(f"   Winner: {winner}")
            
            return analysis
            
        except Exception as e:
            self.log_collection(f"❌ Error during comparison: {e}")
            return None
    
    def run_continuous(self, interval_minutes: int = 60, total_runs: int = None):
        """
        Run comparisons continuously at regular intervals
        
        Args:
            interval_minutes: Minutes between comparisons
            total_runs: Total number of runs (None = infinite)
        """
        print("\n" + "=" * 80)
        print("🤖 AUTOMATED DATA COLLECTION")
        print("=" * 80)
        print(f"Interval: {interval_minutes} minutes")
        print(f"Total runs: {total_runs if total_runs else 'Continuous'}")
        print(f"Data directory: {self.data_directory}")
        print("=" * 80)
        print("\nPress Ctrl+C to stop collection\n")
        
        run_count = 0
        
        try:
            while True:
                run_count += 1
                
                if total_runs and run_count > total_runs:
                    self.log_collection(f"✅ Completed {total_runs} runs. Stopping.")
                    break
                
                self.log_collection(f"📊 Run #{run_count}")
                self.log_collection("=" * 80)
                
                # Run comparison
                result = self.run_single_comparison()
                
                if result:
                    self.log_collection(f"✅ Run #{run_count} completed successfully")
                else:
                    self.log_collection(f"❌ Run #{run_count} failed")
                
                self.log_collection("=" * 80)
                
                # Check if we should continue
                if total_runs and run_count >= total_runs:
                    break
                
                # Wait for next run
                self.log_collection(f"⏳ Waiting {interval_minutes} minutes until next run...")
                time.sleep(interval_minutes * 60)
                
        except KeyboardInterrupt:
            print("\n\n" + "=" * 80)
            print("🛑 DATA COLLECTION STOPPED")
            print("=" * 80)
            print(f"Total runs completed: {run_count}")
            print(f"Data saved in: {self.data_directory}")
            print("=" * 80)
    
    def run_scheduled(self, times_per_day: int = 3, days: int = 7):
        """
        Run comparisons at specific times throughout the day
        
        Args:
            times_per_day: Number of comparisons per day (evenly spaced)
            days: Number of days to collect data
        """
        interval_minutes = (24 * 60) // times_per_day
        total_runs = times_per_day * days
        
        print("\n" + "=" * 80)
        print("📅 SCHEDULED DATA COLLECTION")
        print("=" * 80)
        print(f"Times per day: {times_per_day}")
        print(f"Days to collect: {days}")
        print(f"Total runs: {total_runs}")
        print(f"Interval: ~{interval_minutes} minutes ({interval_minutes/60:.1f} hours)")
        print("=" * 80)
        print()
        
        self.log_collection(f"Starting scheduled collection: {times_per_day}x/day for {days} days")
        
        self.run_continuous(interval_minutes, total_runs)


def main():
    """Main execution"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                  AUTOMATED DATA COLLECTION                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

This script runs algorithm comparisons regularly and saves all results.

Choose a mode:
  1. Continuous (runs every X minutes indefinitely)
  2. Scheduled (runs X times per day for Y days)
  3. Quick Test (runs 3 times, 5 minutes apart)
    """)
    
    choice = input("Enter choice (1/2/3): ").strip()
    
    collector = DataCollector(data_directory="comparison_data")
    
    if choice == "1":
        print("\n📊 CONTINUOUS MODE")
        interval = input("Enter interval in minutes (default 60): ").strip()
        interval = int(interval) if interval else 60
        
        collector.run_continuous(interval_minutes=interval)
        
    elif choice == "2":
        print("\n📅 SCHEDULED MODE")
        times_per_day = input("Times per day (default 3): ").strip()
        times_per_day = int(times_per_day) if times_per_day else 3
        
        days = input("Number of days (default 7): ").strip()
        days = int(days) if days else 7
        
        collector.run_scheduled(times_per_day=times_per_day, days=days)
        
    elif choice == "3":
        print("\n🧪 QUICK TEST MODE")
        print("Running 3 comparisons, 5 minutes apart...\n")
        
        collector.run_continuous(interval_minutes=5, total_runs=3)
        
    else:
        print("\n❌ Invalid choice. Exiting.")
        return
    
    print("\n✅ Data collection complete!")
    print(f"📁 All results saved in: {collector.data_directory}/")
    print("\nNext step: Run 'python3 batch_analysis.py' to analyze all collected data\n")


if __name__ == "__main__":
    main()
