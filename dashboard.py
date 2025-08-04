import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import os
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class DisasterLawAnalyzer:
    def __init__(self):
        self.combined_data = pd.DataFrame()
        self.file_metadata = []
        
        # Color palette - Blue and Yellow theme
        self.colors = {
            'primary': '#1f4e79',
            'secondary': '#ffd60a', 
            'accent': '#4895d9',
            'light': '#ffed4e',
            'palette': ['#1f4e79', '#ffd60a', '#4895d9', '#ffed4e', '#28a745', '#dc3545']
        }
        
        # Regional mapping based on filename patterns
        self.region_mapping = {
            'AKHI': 'Alaska/Hawaii',
            'Appalachia': 'Appalachia/Central',
            'CAWA': 'CA/WA/OR',
            'Midwest': 'Midwest',
            'MTN': 'Mountain West',
            'Northeast': 'Northeast',
            'Southern': 'Southern/Mid-Atlantic',
            'MidAtlantic': 'Southern/Mid-Atlantic'
        }
    
    def load_all_datasets(self, folder_path='.'):
        """Load and combine all Excel files in the folder"""
        excel_files = [
            'AKHIKeyStatutesCodesLocalAuthorityNotableProvisionsVulnerablePopulationsProtections.xlsx',
            'AppalachiaCentralKeyStatutesCodesLocalAuthorityNotableProvisionsVulnerablePopulationsProtections1.xlsx',
            'ApproachExampleStatusinMidwest.xlsx',
            'AspectSouthernStatesMidAtlanticStates.xlsx',
            'CAWAORCivilRightsNonDiscriminationDisabilityFunctionalNeedsLanguageAccessEquityInitiatives.xlsx',
            'CAWAOREmertives.xlsx',
            'CAWAORKeyStatutesCodesLocalAuthorityNotableProvisionsVulnerablePopulationsProtections.xlsx',
            'ComparisonFocus.xlsx',
            'ImpactAreaSouthernStatesMidAtlanticStates.xlsx',
            'MidwestEmergencyDeclarationLocalEmergencyPowersMitigationPlanningMutualAidVulnerablePopulationProvisions.xlsx',
            'MidwestKeyStatutesCodesLocalAuthorityNotableProvisionsVulnerablePopulationsProtections.xlsx',
            'MidwestStateEmergencyDeclarationLocalEmergencyPowersMitigationPlanningMutualAidExplicitVulnerablePopulationsProtections.xlsx',
            'MTNWestKeyStatutesCodesLocalAuthorityNotableProvisionsVulnerablePopulationsProtections.xlsx',
            'NortheastKeyStatutesCodesLocalAuthorityNotableProvisionsVulnerablePopulationsProtections 2.xlsx',
            'ProtectionAreaRiskWithoutFEMASupport.xlsx'
        ]
        
        all_data = []
        
        for filename in excel_files:
            filepath = os.path.join(folder_path, filename)
            if os.path.exists(filepath):
                try:
                    # Read all sheets in the Excel file
                    excel_file = pd.ExcelFile(filepath)
                    
                    for sheet_name in excel_file.sheet_names:
                        df = pd.read_excel(filepath, sheet_name=sheet_name)
                        
                        # Add metadata columns
                        df['source_file'] = filename
                        df['sheet_name'] = sheet_name
                        df['region'] = self._extract_region(filename)
                        df['theme'] = self._extract_theme(filename)
                        
                        # Clean empty rows
                        df = df.dropna(how='all')
                        
                        all_data.append(df)
                        
                        # Store metadata
                        self.file_metadata.append({
                            'filename': filename,
                            'sheet_name': sheet_name,
                            'rows': len(df),
                            'columns': len(df.columns),
                            'region': self._extract_region(filename),
                            'theme': self._extract_theme(filename)
                        })
                        
                        print(f"✅ Loaded: {filename} ({sheet_name}) - {len(df)} rows")
                        
                except Exception as e:
                    print(f"❌ Error loading {filename}: {str(e)}")
                    
        if all_data:
            self.combined_data = pd.concat(all_data, ignore_index=True, sort=False)
            print(f"\n🎉 Successfully combined {len(all_data)} datasets")
            print(f"📊 Total records: {len(self.combined_data)}")
            print(f"📋 Total columns: {len(self.combined_data.columns)}")
            
        return self.combined_data
    
    def _extract_region(self, filename):
        """Extract region from filename"""
        for key, region in self.region_mapping.items():
            if key in filename:
                return region
        return 'Other'
    
    def _extract_theme(self, filename):
        """Extract theme from filename"""
        if 'KeyStatutes' in filename or 'LocalAuthority' in filename:
            return 'Legal Framework'
        elif 'Emergency' in filename or 'Declaration' in filename:
            return 'Emergency Management'
        elif 'Vulnerable' in filename or 'Protection' in filename:
            return 'Vulnerable Populations'
        elif 'CivilRights' in filename or 'Equity' in filename:
            return 'Civil Rights/Equity'
        elif 'FEMA' in filename or 'Risk' in filename:
            return 'FEMA/Risk Assessment'
        else:
            return 'General'
    
    def create_overview_dashboard(self):
        """Create comprehensive overview visualizations"""
        
        # Create subplot figure
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Datasets by Region', 'Datasets by Theme', 
                          'Records by Region', 'Data Coverage Heatmap'),
            specs=[[{"type": "bar"}, {"type": "pie"}],
                   [{"type": "bar"}, {"type": "heatmap"}]]
        )
        
        # 1. Datasets by Region
        region_counts = pd.DataFrame(self.file_metadata).groupby('region').size().reset_index()
        region_counts.columns = ['region', 'count']
        
        fig.add_trace(
            go.Bar(x=region_counts['region'], y=region_counts['count'],
                   marker_color=self.colors['primary'], name='Datasets'),
            row=1, col=1
        )
        
        # 2. Datasets by Theme (Pie Chart)
        theme_counts = pd.DataFrame(self.file_metadata).groupby('theme').size().reset_index()
        theme_counts.columns = ['theme', 'count']
        
        fig.add_trace(
            go.Pie(labels=theme_counts['theme'], values=theme_counts['count'],
                   marker_colors=self.colors['palette'][:len(theme_counts)]),
            row=1, col=2
        )
        
        # 3. Records by Region
        metadata_df = pd.DataFrame(self.file_metadata)
        records_by_region = metadata_df.groupby('region')['rows'].sum().reset_index()
        
        fig.add_trace(
            go.Bar(x=records_by_region['region'], y=records_by_region['rows'],
                   marker_color=self.colors['secondary'], name='Records'),
            row=2, col=1
        )
        
        # 4. Coverage Heatmap
        coverage_matrix = metadata_df.pivot_table(
            values='rows', index='region', columns='theme', 
            aggfunc='sum', fill_value=0
        )
        
        fig.add_trace(
            go.Heatmap(z=coverage_matrix.values,
                      x=coverage_matrix.columns,
                      y=coverage_matrix.index,
                      colorscale='Blues'),
            row=2, col=2
        )
        
        fig.update_layout(
            height=800,
            title_text="Disaster Law Datasets - Comprehensive Overview",
            title_x=0.5,
            showlegend=False
        )
        
        return fig
    
    def analyze_local_authority(self):
        """Analyze Local Authority patterns across regions"""
        if 'Local Authority' not in self.combined_data.columns:
            print("❌ 'Local Authority' column not found in combined data")
            return None
            
        # Clean and standardize Local Authority values
        self.combined_data['Local Authority Clean'] = self.combined_data['Local Authority'].str.lower().str.strip()
        
        authority_by_region = self.combined_data.groupby(['region', 'Local Authority Clean']).size().unstack(fill_value=0)
        
        fig = px.bar(
            authority_by_region.reset_index(),
            x='region',
            y=['yes', 'no'] if 'yes' in authority_by_region.columns and 'no' in authority_by_region.columns else authority_by_region.columns.tolist(),
            title="Local Authority Enabled by Region",
            color_discrete_sequence=[self.colors['primary'], self.colors['secondary']]
        )
        
        fig.update_layout(
            xaxis_title="Region",
            yaxis_title="Number of Records",
            legend_title="Local Authority"
        )
        
        return fig
    
    def analyze_vulnerable_populations(self):
        """Analyze vulnerable population protections"""
        if 'Vulnerable Populations Protections' not in self.combined_data.columns:
            print("❌ 'Vulnerable Populations Protections' column not found")
            return None
            
        # Check for non-null vulnerable population protections
        vuln_pop_data = self.combined_data.groupby('region').agg({
            'Vulnerable Populations Protections': ['count', lambda x: x.notna().sum()]
        }).round(2)
        
        vuln_pop_data.columns = ['Total Records', 'Has Protection']
        vuln_pop_data['Protection Rate'] = (vuln_pop_data['Has Protection'] / vuln_pop_data['Total Records'] * 100).round(1)
        vuln_pop_data = vuln_pop_data.reset_index()
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=vuln_pop_data['region'],
            y=vuln_pop_data['Has Protection'],
            name='Has Protection',
            marker_color=self.colors['primary']
        ))
        
        fig.add_trace(go.Bar(
            x=vuln_pop_data['region'],
            y=vuln_pop_data['Total Records'] - vuln_pop_data['Has Protection'],
            name='No Protection',
            marker_color=self.colors['secondary']
        ))
        
        fig.update_layout(
            title="Vulnerable Population Protections by Region",
            xaxis_title="Region",
            yaxis_title="Number of Records",
            barmode='stack'
        )
        
        return fig
    
    def create_state_summary(self):
        """Create state-by-state summary if State column exists"""
        if 'State' not in self.combined_data.columns:
            print("❌ 'State' column not found")
            return None
            
        state_summary = self.combined_data.groupby('State').agg({
            'Local Authority': lambda x: (x.str.lower() == 'yes').sum(),
            'Vulnerable Populations Protections': lambda x: x.notna().sum(),
            'region': 'first',
            'theme': 'count'
        }).rename(columns={
            'Local Authority': 'Local Authority Count',
            'Vulnerable Populations Protections': 'Vuln Pop Protection Count',
            'theme': 'Total Records'
        })
        
        return state_summary.reset_index()
    
    def export_combined_data(self, filename='combined_disaster_law_data.csv'):
        """Export the combined dataset"""
        if not self.combined_data.empty:
            self.combined_data.to_csv(filename, index=False)
            print(f"✅ Combined data exported to: {filename}")
            print(f"📊 Shape: {self.combined_data.shape}")
            return filename
        else:
            print("❌ No data to export")
            return None
    
    def generate_summary_report(self):
        """Generate a comprehensive summary report"""
        if self.combined_data.empty:
            print("❌ No data loaded. Please run load_all_datasets() first.")
            return
            
        print("\n" + "="*60)
        print("📋 DISASTER LAW DATASET SUMMARY REPORT")
        print("="*60)
        
        print(f"\n📊 OVERALL STATISTICS:")
        print(f"   • Total Files Processed: {len(set([m['filename'] for m in self.file_metadata]))}")
        print(f"   • Total Sheets: {len(self.file_metadata)}")
        print(f"   • Total Records: {len(self.combined_data):,}")
        print(f"   • Total Columns: {len(self.combined_data.columns)}")
        
        print(f"\n🗺️ REGIONAL BREAKDOWN:")
        region_stats = pd.DataFrame(self.file_metadata).groupby('region').agg({
            'filename': 'count',
            'rows': 'sum'
        }).rename(columns={'filename': 'datasets', 'rows': 'total_records'})
        
        for region, stats in region_stats.iterrows():
            print(f"   • {region}: {stats['datasets']} datasets, {stats['total_records']:,} records")
        
        print(f"\n🏷️ THEMATIC BREAKDOWN:")
        theme_stats = pd.DataFrame(self.file_metadata).groupby('theme').agg({
            'filename': 'count',
            'rows': 'sum'
        }).rename(columns={'filename': 'datasets', 'rows': 'total_records'})
        
        for theme, stats in theme_stats.iterrows():
            print(f"   • {theme}: {stats['datasets']} datasets, {stats['total_records']:,} records")
        
        # Column analysis
        print(f"\n📋 COMMON COLUMNS:")
        column_counts = {}
        for col in self.combined_data.columns:
            if col not in ['source_file', 'sheet_name', 'region', 'theme']:
                column_counts[col] = self.combined_data[col].notna().sum()
        
        for col, count in sorted(column_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            coverage = (count / len(self.combined_data) * 100)
            print(f"   • {col}: {count:,} records ({coverage:.1f}% coverage)")
        
        print("\n" + "="*60)

# Usage example
if __name__ == "__main__":
    # Initialize the analyzer
    analyzer = DisasterLawAnalyzer()
    
    # Load all datasets
    print("🚀 Loading disaster law datasets...")
    combined_data = analyzer.load_all_datasets()
    
    # Generate summary report
    analyzer.generate_summary_report()
    
    # Create visualizations
    print("\n📊 Creating visualizations...")
    
    # 1. Overview dashboard
    overview_fig = analyzer.create_overview_dashboard()
    overview_fig.write_html("disaster_law_overview.html")
    print("✅ Overview dashboard saved: disaster_law_overview.html")
    
    # 2. Local Authority analysis
    authority_fig = analyzer.analyze_local_authority()
    if authority_fig:
        authority_fig.write_html("local_authority_analysis.html")
        print("✅ Local Authority analysis saved: local_authority_analysis.html")
    
    # 3. Vulnerable Populations analysis
    vuln_pop_fig = analyzer.analyze_vulnerable_populations()
    if vuln_pop_fig:
        vuln_pop_fig.write_html("vulnerable_populations_analysis.html")
        print("✅ Vulnerable Populations analysis saved: vulnerable_populations_analysis.html")
    
    # 4. Export combined data
    analyzer.export_combined_data()
    
    # 5. Create state summary if available
    state_summary = analyzer.create_state_summary()
    if state_summary is not None:
        state_summary.to_csv('state_summary.csv', index=False)
        print("✅ State summary saved: state_summary.csv")
    
    print("\n🎉 Analysis complete! Open the HTML files in your browser to view interactive visualizations.")
