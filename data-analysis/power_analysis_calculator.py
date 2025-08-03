"""
A/B Test Power Analysis Calculator

This script calculates sample sizes and test durations for different 
Minimum Detectable Effects (MDE) in A/B testing experiments.

Key Formulas:
- Sample Size: n = 2 * (Z_α/2 + Z_β)² * p(1-p) / (MDE)²
- Duration: Total Sample Size ÷ (Monthly Population ÷ 30)

Usage:
    from power_analysis_calculator import PowerAnalysisCalculator
    
    calculator = PowerAnalysisCalculator(
        baseline_rate=0.05,
        monthly_population=100000,
        num_variants=2,
        power=0.8,
        alpha=0.05
    )
    
    results = calculator.calculate_power_analysis()
    calculator.display_results()
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt


class PowerAnalysisCalculator:
    def __init__(self, baseline_rate=0.05, monthly_population=100000, 
                 num_variants=2, power=0.8, alpha=0.05):
        """
        Initialize the power analysis calculator.
        
        Parameters:
        -----------
        baseline_rate : float
            Baseline conversion rate (as decimal, e.g., 0.05 for 5%)
        monthly_population : int
            Total users/sessions available per month
        num_variants : int
            Number of variants including control (typically 2)
        power : float
            Statistical power (typically 0.8 for 80%)
        alpha : float
            Significance level (typically 0.05 for 95% confidence)
        """
        self.baseline_rate = baseline_rate
        self.monthly_population = monthly_population
        self.num_variants = num_variants
        self.power = power
        self.alpha = alpha
        
        # Calculate critical values
        self.z_alpha_2 = stats.norm.ppf(1 - alpha/2)  # Two-tailed test
        self.z_beta = stats.norm.ppf(power)
        
    def calculate_sample_size(self, mde):
        """
        Calculate sample size per variant for given MDE.
        
        Formula: n = 2 * (Z_α/2 + Z_β)² * p(1-p) / (MDE)²
        
        Parameters:
        -----------
        mde : float
            Minimum detectable effect (as decimal)
            
        Returns:
        --------
        int : Sample size per variant
        """
        p = self.baseline_rate
        numerator = 2 * (self.z_alpha_2 + self.z_beta)**2 * p * (1 - p)
        denominator = mde**2
        return int(np.ceil(numerator / denominator))
    
    def calculate_power_analysis(self, mde_range=None):
        """
        Calculate power analysis for a range of MDE values.
        
        Parameters:
        -----------
        mde_range : list, optional
            List of MDE percentages to analyze (default: 1% to 30%)
            
        Returns:
        --------
        pd.DataFrame : Power analysis results
        """
        if mde_range is None:
            mde_range = list(range(1, 31))  # 1% to 30%
        
        results = []
        
        for mde_percent in mde_range:
            mde_decimal = mde_percent / 100
            
            # Calculate sample sizes
            sample_size_per_variant = self.calculate_sample_size(mde_decimal)
            total_sample_size = sample_size_per_variant * self.num_variants
            
            # Calculate duration and feasibility metrics
            population_split_percent = (total_sample_size / self.monthly_population) * 100
            daily_population = self.monthly_population / 30  # Daily traffic
            duration_days = total_sample_size / daily_population  # Days needed to collect sample
            duration_weeks = duration_days / 7
            
            # Determine feasibility
            if duration_days <= 7:
                feasibility = "Very Short"
            elif duration_days <= 14:
                feasibility = "Short"
            elif duration_days <= 30:
                feasibility = "Moderate"
            else:
                feasibility = "Long"
            
            # Traffic requirement assessment
            if population_split_percent <= 25:
                traffic_assessment = "Excellent"
            elif population_split_percent <= 50:
                traffic_assessment = "Good"
            elif population_split_percent <= 75:
                traffic_assessment = "Challenging"
            else:
                traffic_assessment = "Insufficient Traffic"
            
            results.append({
                'MDE_Percent': mde_percent,
                'MDE_Decimal': mde_decimal,
                'Sample_Size_Per_Variant': sample_size_per_variant,
                'Total_Sample_Size': total_sample_size,
                'Population_Split_Percent': round(population_split_percent, 2),
                'Duration_Days': round(duration_days, 2),
                'Duration_Weeks': round(duration_weeks, 2),
                'Feasibility': feasibility,
                'Traffic_Assessment': traffic_assessment
            })
        
        self.results_df = pd.DataFrame(results)
        return self.results_df
    
    def display_results(self, top_n=None):
        """
        Display formatted results.
        
        Parameters:
        -----------
        top_n : int, optional
            Number of top results to display (default: all)
        """
        if not hasattr(self, 'results_df'):
            self.calculate_power_analysis()
        
        print("=" * 80)
        print("A/B TEST POWER ANALYSIS RESULTS")
        print("=" * 80)
        print(f"Input Parameters:")
        print(f"  Baseline Conversion Rate: {self.baseline_rate:.1%}")
        print(f"  Monthly Population: {self.monthly_population:,}")
        print(f"  Number of Variants: {self.num_variants}")
        print(f"  Statistical Power: {self.power:.1%}")
        print(f"  Significance Level: {self.alpha:.1%}")
        print("-" * 80)
        
        df_display = self.results_df.copy()
        if top_n:
            df_display = df_display.head(top_n)
        
        # Format for display
        print(f"{'MDE':<6} {'Sample/Var':<12} {'Total':<10} {'Pop %':<8} {'Days':<8} {'Weeks':<8} {'Feasibility':<12}")
        print("-" * 80)
        
        for _, row in df_display.iterrows():
            print(f"{row['MDE_Percent']:>3}%   "
                  f"{row['Sample_Size_Per_Variant']:>8,}    "
                  f"{row['Total_Sample_Size']:>7,}   "
                  f"{row['Population_Split_Percent']:>5.1f}%   "
                  f"{row['Duration_Days']:>5.1f}   "
                  f"{row['Duration_Weeks']:>5.1f}   "
                  f"{row['Feasibility']:<12}")
    
    def get_recommendations(self):
        """
        Get recommendations based on the power analysis.
        
        Returns:
        --------
        dict : Recommendations for different scenarios
        """
        if not hasattr(self, 'results_df'):
            self.calculate_power_analysis()
        
        # Filter for reasonable durations and traffic requirements
        feasible = self.results_df[
            (self.results_df['Duration_Days'] <= 30) & 
            (self.results_df['Population_Split_Percent'] <= 50)
        ]
        
        recommendations = {
            'quick_test': None,
            'standard_test': None,
            'sensitive_test': None
        }
        
        # Quick test (< 1 week)
        quick = feasible[feasible['Duration_Days'] <= 7]
        if not quick.empty:
            recommendations['quick_test'] = {
                'mde': quick.iloc[-1]['MDE_Percent'],  # Highest feasible MDE
                'duration': quick.iloc[-1]['Duration_Days'],
                'sample_size': quick.iloc[-1]['Total_Sample_Size']
            }
        
        # Standard test (1-3 weeks)
        standard = feasible[
            (feasible['Duration_Days'] > 7) & 
            (feasible['Duration_Days'] <= 21)
        ]
        if not standard.empty:
            mid_idx = len(standard) // 2
            recommendations['standard_test'] = {
                'mde': standard.iloc[mid_idx]['MDE_Percent'],
                'duration': standard.iloc[mid_idx]['Duration_Days'],
                'sample_size': standard.iloc[mid_idx]['Total_Sample_Size']
            }
        
        # Sensitive test (lowest feasible MDE)
        if not feasible.empty:
            recommendations['sensitive_test'] = {
                'mde': feasible.iloc[0]['MDE_Percent'],  # Lowest MDE
                'duration': feasible.iloc[0]['Duration_Days'],
                'sample_size': feasible.iloc[0]['Total_Sample_Size']
            }
        
        return recommendations
    
    def plot_power_curve(self, save_path=None):
        """
        Create a visualization of the power analysis results.
        
        Parameters:
        -----------
        save_path : str, optional
            Path to save the plot
        """
        if not hasattr(self, 'results_df'):
            self.calculate_power_analysis()
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('A/B Test Power Analysis', fontsize=16, fontweight='bold')
        
        df = self.results_df
        
        # Sample size vs MDE
        ax1.plot(df['MDE_Percent'], df['Sample_Size_Per_Variant'], 
                marker='o', linewidth=2, markersize=6)
        ax1.set_xlabel('Minimum Detectable Effect (%)')
        ax1.set_ylabel('Sample Size per Variant')
        ax1.set_title('Sample Size vs MDE')
        ax1.grid(True, alpha=0.3)
        ax1.set_yscale('log')
        
        # Duration vs MDE
        colors = ['red' if x > 30 else 'orange' if x > 14 else 'green' 
                 for x in df['Duration_Days']]
        ax2.scatter(df['MDE_Percent'], df['Duration_Days'], 
                   c=colors, alpha=0.7, s=50)
        ax2.set_xlabel('Minimum Detectable Effect (%)')
        ax2.set_ylabel('Duration (Days)')
        ax2.set_title('Test Duration vs MDE')
        ax2.grid(True, alpha=0.3)
        ax2.axhline(y=14, color='orange', linestyle='--', alpha=0.5, label='2 weeks')
        ax2.axhline(y=30, color='red', linestyle='--', alpha=0.5, label='1 month')
        ax2.legend()
        
        # Population split
        ax3.bar(df['MDE_Percent'], df['Population_Split_Percent'], 
               color=['red' if x > 75 else 'orange' if x > 50 else 'green' 
                      for x in df['Population_Split_Percent']])
        ax3.set_xlabel('Minimum Detectable Effect (%)')
        ax3.set_ylabel('Population Split (%)')
        ax3.set_title('Traffic Requirement vs MDE')
        ax3.grid(True, alpha=0.3)
        ax3.axhline(y=50, color='orange', linestyle='--', alpha=0.5, label='50% traffic')
        ax3.legend()
        
        # Feasibility heatmap
        feasibility_map = {'Very Short': 4, 'Short': 3, 'Moderate': 2, 'Long': 1}
        feasibility_scores = [feasibility_map[f] for f in df['Feasibility']]
        
        scatter = ax4.scatter(df['MDE_Percent'], df['Population_Split_Percent'], 
                            c=feasibility_scores, cmap='RdYlGn', 
                            s=100, alpha=0.7)
        ax4.set_xlabel('Minimum Detectable Effect (%)')
        ax4.set_ylabel('Population Split (%)')
        ax4.set_title('Feasibility Map')
        ax4.grid(True, alpha=0.3)
        
        # Add colorbar
        cbar = plt.colorbar(scatter, ax=ax4)
        cbar.set_label('Feasibility')
        cbar.set_ticks([1, 2, 3, 4])
        cbar.set_ticklabels(['Long', 'Moderate', 'Short', 'Very Short'])
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def export_to_csv(self, filename='power_analysis_results.csv'):
        """
        Export results to CSV file.
        
        Parameters:
        -----------
        filename : str
            Output filename
        """
        if not hasattr(self, 'results_df'):
            self.calculate_power_analysis()
        
        self.results_df.to_csv(filename, index=False)
        print(f"Results exported to {filename}")


# Example usage
if __name__ == "__main__":
    # Example: E-commerce conversion rate optimization
    calculator = PowerAnalysisCalculator(
        baseline_rate=0.03,      # 3% conversion rate
        monthly_population=50000, # 50K monthly users
        num_variants=2,          # A/B test (control + treatment)
        power=0.8,              # 80% power
        alpha=0.05              # 95% confidence
    )
    
    # Calculate and display results
    results = calculator.calculate_power_analysis()
    calculator.display_results(top_n=15)
    
    # Get recommendations
    print("\n" + "="*80)
    print("RECOMMENDATIONS")
    print("="*80)
    
    recs = calculator.get_recommendations()
    
    if recs['quick_test']:
        print(f"Quick Test (< 1 week):")
        print(f"  MDE: {recs['quick_test']['mde']}%")
        print(f"  Duration: {recs['quick_test']['duration']:.1f} days")
        print(f"  Sample Size: {recs['quick_test']['sample_size']:,}")
        print()
    
    if recs['standard_test']:
        print(f"Standard Test (1-3 weeks):")
        print(f"  MDE: {recs['standard_test']['mde']}%")
        print(f"  Duration: {recs['standard_test']['duration']:.1f} days")
        print(f"  Sample Size: {recs['standard_test']['sample_size']:,}")
        print()
    
    if recs['sensitive_test']:
        print(f"Sensitive Test (highest precision):")
        print(f"  MDE: {recs['sensitive_test']['mde']}%")
        print(f"  Duration: {recs['sensitive_test']['duration']:.1f} days")
        print(f"  Sample Size: {recs['sensitive_test']['sample_size']:,}")