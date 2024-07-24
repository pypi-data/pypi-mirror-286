'''
Original script from BETTER: https://github.com/LBNL-JCI-ICF/better

'''

import datetime
import numpy as np
from . import constants
import os
import plotly.graph_objects as go
from plotly.io import to_html as plt_to_html

class Report:

    def __init__(self, building=None, portfolio=None):
        self.logo()
        if building != None:
            self.building = building
            self.currency_str = building.currency
            if "us dollar" in building.currency.lower():
                self.currency_str = '$'
            if "euro" in building.currency.lower():
                self.currency_str = '€'
            
            self.charts_js()
        if portfolio != None:
            self.portfolio = portfolio

    @staticmethod
    def format_number(number):
        str_number = ''
        try:
            str_number = '{:,}'.format(number)
        except:
            str_number = str(number)
        return str_number

    @staticmethod
    def html_basic():
        html_text =  '''
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
            <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Raleway">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
            <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.4.0/Chart.min.js"></script>
            <script type="text/javascript" src="https://code.jquery.com/jquery-3.3.1.js"></script>
            <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery.tablesorter/2.31.0/js/jquery.tablesorter.js"></script>
            <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/plotly.js/1.42.5/plotly.js"></script>
            <style>
            body,
            h1,
            h2,
            h3,
            h4,
            h5,
            h6 {
                font-family: "Helvetica", sans-serif
                }
            .td_border {
                border: solid 0px grey;
                }
            .w3-table td {
                padding: 0px;
                }
            .number {
                position: relative;
                font: bold italic 45px/1.5 Helvetica, Verdana, sans-serif;
                color: green;
                margin: 10px;
                text-align: left;
                }
            .benchmark_bar {
                height: 38px;
                background: linear-gradient(to right, #ff0000 0%, #ffff00 50%, #00ff00 100%);
                }
            .vertical_line {
                height: 38px;
                width: 3px;
                background: #000;
                position: relative;
                }
            </style>
        '''
        return html_text

    def navigation_bar(self):
        html_text = ''
        # Navigation bar
        html_text += '<nav class="w3-sidebar w3-collapse w3-white w3-animate-left" style="z-index:3;width:270px;" id="mySidebar"><br>'
        html_text += '    <div class="w3-container">'
        html_text += '        <a href="#" onclick="w3_close()" class="w3-hide-large w3-right w3-jumbo w3-padding w3-hover-grey" title="close menu">'
        html_text += '            <i class="fa fa-remove"></i>'
        html_text += '        </a>'
        html_text += self.equans_logo
        html_text += self.icf_logo
        html_text += self.jci_logo
        html_text += '        <br><br>'
        html_text += '        <h4><b>Building Efficiency Targeting Tool for Energy Retrofits (BETTER)</b></h4>'
        html_text += '        <p class="w3-text-grey">' + datetime.datetime.now().strftime("%Y-%m-%d  %H:%M") + '</p>'
        html_text += '    </div>'
        html_text += '    <div class="w3-bar-block">'
        html_text += '        <a href="#overview" onclick="w3_close()" class="w3-bar-item w3-button w3-padding"><i class="fa fa-th-large fa-fw w3-margin-right"></i>Overview</a> '
        html_text += '        <a href="#benchmark" onclick="w3_close()" class="w3-bar-item w3-button w3-padding"><i class="fa fa-group fa-fw w3-margin-right"></i>Benchmark</a> '
        html_text += '        <a href="#EE" onclick="w3_close()" class="w3-bar-item w3-button w3-padding"><i class="fa fa-calculator fa-fw w3-margin-right"></i>Energy Efficiency Analysis</a>'
        html_text += '        <a href="#IMT" onclick="w3_close()" class="w3-bar-item w3-button w3-padding"><i class="fa fa-key fa-fw w3-margin-right"></i>Performance Key</a>'
        html_text += '        <a href="#About" onclick="w3_close()" class="w3-bar-item w3-button w3-padding"><i class="fa fa-info fa-fw w3-margin-right"></i>About BETTER</a>'
        html_text += '    </div>'
        html_text += '</nav>'

        # Overlay effect when opening sidebar on small screens
        html_text += '<div class="w3-overlay w3-hide-large w3-animate-opacity" onclick="w3_close()" style="cursor:pointer" title="close side menu" id="myOverlay"></div>'
        html_text += '<!-- !PAGE CONTENT! -->'
        html_text += '<div class="w3-main" style="margin-left:300px; margin-right:20px">'
        return html_text
    

    def generate_building_report_html_with_jinja(self):

        from jinja2 import Environment, FileSystemLoader
        from pathlib import Path
        templates_path = os.path.join(
            Path(__file__).resolve(strict=True).parent,
            "templates"
        )
        environment = Environment(loader=FileSystemLoader(templates_path))
        if hasattr(self.building,"weather_electricity") and self.building.weather_electricity:
            weather_instance = self.building.weather_electricity
        elif hasattr(self.building,"weather_fossil_fuel") and self.building.weather_fossil_fuel:
            weather_instance = self.building.weather_fossil_fuel
        else:
            weather_instance = None

        report_content_template = environment.get_template("building_analytic_report_content.html")

        ##### horizontal bar charts ####        
        saving_bar_graph_data = [
            go.Bar(
                y = ["Current", "Typical", "Target"],
                x = [
                    self.building.cooling_old_cost, 
                    self.building.cooling_typical_cost,
                    self.building.cooling_new_cost
                ],
                name="Cooling",
                orientation="h",
                marker=dict(
                    color='rgba(31,78,121,1)'
                )
            ),
            go.Bar(
                y = ["Current", "Typical", "Target"],
                x = [
                    self.building.base_old_cost, 
                    self.building.base_typical_cost,
                    self.building.base_new_cost
                ],
                name="Baseload",
                orientation="h",
                marker=dict(
                    color='rgba(127,127,127,1)'
                )
            ),
            go.Bar(
                y = ["Current", "Typical", "Target"],
                x = [
                    self.building.heating_old_cost, 
                    self.building.heating_typical_cost,
                    self.building.heating_new_cost
                ],
                name="Heating",
                orientation="h",
                marker=dict(
                    color='rgba(192,0,0,1)'
                )
            )
        ]
        saving_bar_fig = go.Figure(
            data= saving_bar_graph_data
        )
        saving_bar_fig.update_layout(
            title = f"<b>Cost Breakdown (k{self.currency_str})</b>",
            titlefont = dict(
                family = "sans-serif",
                size = 18
            ),
            barmode='stack',
            xaxis = dict(
                tickfont = dict(
                    family = "sans-serif",
                    size = 16
                )
            ),
            yaxis = dict(
                tickfont = dict(
                    family = "sans-serif",
                    size = 16
                )
            ),
            legend = dict(
                orientation='h',
                font = dict(
                    family = "sans-serif",
                    size = 16
                ),
                xanchor = "center",
                x = 0.5
            ),
            height = 500
        )
        saving_bar_fig_html = plt_to_html(
            saving_bar_fig,
            include_plotlyjs=False,
            full_html=False,
            div_id="saving_bar_chart"
        )

        ## Saving pie chart
        saving_pie_graph_data = [
            go.Pie(
                labels = ["Cooling", "Baseload", "Heating"],
                values = [
                    self.building.cooling_old_cost - self.building.cooling_new_cost,
                    self.building.base_old_cost - self.building.base_new_cost,
                    self.building.heating_old_cost - self.building.heating_new_cost
                ],
                hole=.5,
                marker_colors = ['rgba(31,78,121,1)','rgba(127,127,127,1)','rgba(192,0,0,1)']
            )
        ]
        saving_pie_fig = go.Figure(
            data=saving_pie_graph_data
        )
        saving_pie_fig.update_layout(
            title = f"<b>Cost Savings Breakdown ({self.currency_str})</b>",
            titlefont = dict(
                family = "sans-serif",
                size = 18
            ),
            legend = dict(
                orientation='h',
                font = dict(
                    family = "sans-serif",
                    size = 16
                ),
                xanchor = "center",
                x = 0.5,
                yanchor = 'top',
                y = -0.2
            ),
            height = 500
        )

        saving_pie_fig_html = plt_to_html(
            saving_pie_fig,
            include_plotlyjs=False,
            full_html=False,
            div_id="saving_pie_chart"
        )

        FIM_des = {
            "Reduce Equipment Schedules": "Your building equipment load is higher than that of a typical building. "
                "Look for opportunities to turn off equipment during times of low occupancy or reduced building use. "
                "A building automation system (BAS) may also be used to schedule equipment and systems that operate within a building. "
                "Routinely check and tune the BAS schedule to ensure it matches occupant needs. "
                "Alarms should be set up and monitored to identify when overridden schedules are not returned to normal.",

            "Reduce Lighting Load": "Your building lighting load is higher than that of a typical building. "
                "Lighting load is a significant portion of any building's energy consumption, but lighting efficiency and controls have a big impact on lighting system performance. "
                "Consider upgrading bulbs and fixtures to improve efficiency and check existing (or upgrade to) controls that dim and turn off the lights appropriately.  "
                "Take advantage of natural daylighting whenever possible. "
                "Lights near existing window or skylights can be controlled to dim or turn off for maximum daylight utilization. "
                "Renovations to the building envelope and internal space configurations are good opportunity to check lighting system performance. ",

            "Reduce Plug Loads": " Your building plug load is higher than that of a typical building. "
                "Anything that is plugged into standard electric receptacles or outlets falls under the “plug load” category. "
                "Personal computers, monitors, printers, coffeemakers, other office/lab/lighting equipment are examples of plug loads. "
                "Consider upgrading to more efficient models and operate on a schedule where possible. "
                "Advanced power strips and other monitoring devices can help you target your most energy-intensive devices.",

            "Increase Cooling System Efficiency": "Your building cooling load is higher than similar buildings for similar weather conditions. HVAC system performance has big impact on building energy consumption. Check your cooling system, all related equipment and controls to improve system efficiency. Upgrading your system to a more efficient model, will reduce your system energy consumption.",

            "Decrease Heating Setpoints": "Your building's heating setpoint is higher than that of a typical building. "
                "Check the occupied and unoccupied heating setpoint during the heating season."
                "Heating system and auxiliaries' energy consumption will be reduced by decreasing the heating setpoint.",
            
            "Ensure Adequate Ventilation Rate": "It is important that the correct amount of fresh air is making its way into the building to provide comfortable and safe conditions for building occupants. "
                "However, if you're providing more fresh air than is necessary for comfort and safety, you may be wasting energy. "
                "Reducing the amount of fresh air, while meeting all health, comfort, and safety requirements, will reduce the energy used to condition and distribute it. "
                "Make sure to understand and follow all building codes, standards, and guidelines related to fresh/outside air ventilation requirements, particularly as pertains to coronavirus (COVID-19).",

            "Decrease Infiltration": "Infiltration is the uncontrolled outside air that is brought into a building. It adds to the overall building cooling and heating loads. Infiltration is reduced with caulking, weather stripping, and upgrades in envelope components (e.g. windows, doors, air intakes and exhausts).",
            "Increase Heating System Efficiency": "Your building heating load is higher than that of a typical building for similar weather conditions. "
                "HVAC system performance has a significant impact on building energy consumption. "
                "Check the heating system, including all related equipment and controls, for efficient operations. "
                "Upgrading your system to a more efficient model will reduce your system's energy consumption.",

            "Add Wall/Ceiling Insulation": "Heating and cooling loads are reduced by insulating the building walls, ceilings, and foundations. Check current insulation levels and assess opportunities of adding more insulation.",
            "Check Fossil Baseload": "Your building thermal load is higher than typical. Check building thermal baseload (minimum continuous usage) for the building. Poor operating schedules, simultaneous heating and cooling, and faulty heating equipment result in higher baseload.",
            "Upgrade Windows": "Windows have big impact on heating and cooling loads. Poor window insulation is like low insulation wall. Check current windows for U-value.",
            "Eliminate Electric Heating": "Your building electric heating load is higher than typical. Electric heating is expensive and increases heating system energy consumption. Check electric heating system schedules and controls. ",
            "Increase Cooling Setpoints" : "Your building starts cooling at lower temperature than typical. Check the occupied and unoccupied cooling setpoint during the cooling season. Cooling system and auxiliaries’ energy consumption will be reduced by increasing the cooling setpoint ",
            "Add/Fix Economizers":"Utilizing outside air that is cooler and/or drier than indoor air in an economizer can significantly reduce the energy used to cool the building. Check existing economizers, if any, for efficient operations."
        }
        #### UPDATE TEMPLATE #####
        html_content = report_content_template.render(
            building = self.building,
            weather_instance = weather_instance,
            currency_str = self.currency_str,
            saving_bar_chart = saving_bar_fig_html,
            saving_pie_chart = saving_pie_fig_html,
            FIM_dict = FIM_des,
            equans_logo=self.equans_logo

        )        
        return (html_content)


    def generate_building_report_html(self):
        html_txt = ""

        # report_html.write('<!DOCTYPE html>')
        # report_html.write('<html>')
        # report_html.write('<title>Building Efficiency Targeting Tool for Energy Retrofits (BETTER) Report</title>')

        # Add basic stuff including css and scripts
        # report_html.write(self.html_basic())

        # report_html.write('<body class="w3-light-grey w3-content" style="max-width:1500px">')
        # report_html.write('<!-- Sidebar/menu -->')

            # Navigation bar
        # report_html.write(self.navigation_bar())

        if self.building.weather_electricity:
            weather_instance = self.building.weather_electricity
        elif self.building.weather_fossil_fuel:
            weather_instance = self.building.weather_fossil_fuel

        #### Building Overview Card #####
        html_txt += '  <div class="w3-container w3-padding-large w3-white">'
        html_txt += '    <h2 id="overview"><b>' + self.building.bldg_name.upper() + '</b></h2>'
        html_txt += '    <hr class="w3-opacity">'

        html_txt += '<div class="w3-container w3-margin-bottom w3-padding-small">'
        # Table 1
        html_txt += '  <table class="w3-table w3-bordered w3-border" style="width:95% border: solid 1 px blue">'
        html_txt += '  <tr>'
        html_txt += '    <td class="td_border" colspan="3"><b>Building Type</b></td>'
        html_txt += '    <td class="td_border" colspan="3">' + self.building.bldg_type + '</td>'
        html_txt += '  </tr>'
        html_txt += '  <tr>'
        html_txt += '    <td class="td_border" colspan="3"><b>Building Location</b></td>'
        html_txt += '    <td class="td_border" colspan="3">' + self.building.bldg_address + '</td>'
        html_txt += '  </tr>'
        html_txt += '  <tr>'
        html_txt += '    <td class="td_border" colspan="3"><b>Gross Floor Area (m<sup>2</sup>)</b></td>'
        html_txt += '    <td class="td_border" colspan="9">' + '{:,}'.format(self.building.bldg_area) + '</td>'
        html_txt += '  </tr>'
        html_txt += '  <tr>'
        html_txt += '    <td class="td_border" colspan="3"><b>Closest Weather Station</b></td>'
        html_txt += '    <td class="td_border" colspan="9">' +f'{weather_instance.closest_weather_station_ID}:{weather_instance.closest_weather_station_name}'+ '</td>'
        html_txt += '  </tr>'
        html_txt += '  </table>'

        html_txt += '  <br>'
        # Table 2
        html_txt += '    <table class="w3-table w3-bordered w3-border" style="width:95% border: solid 1 px blue">'
        html_txt += '  <tr>'
        html_txt += '    <td class="td_border" colspan="4"></td>'
        html_txt += '    <td class="td_border" colspan="4"><b>Electricity</b></td>'
        html_txt += '    <td class="td_border" colspan="4"><b>Fossil Fuel</b></td>'
        html_txt += '  </tr>'
        html_txt += '  <tr>'
        html_txt += '    <td class="td_border" colspan="4"><b>Annual Consumption (kWh)</b></td>'
        if(hasattr(self.building, 'recent_annual_electricity_kWh')):
            html_txt += '    <td class="td_border" colspan="4">' + '{:,}'.format(self.building.recent_annual_electricity_kWh) + '</td>'
        else:
            html_txt += '    <td class="td_border" colspan="4">No electricity data</td>'
        #  html_txt += '    <td class="td_border" colspan="4"><b>Annual Fossil Fuel Consumption (kWh)</b></td>'
        if(hasattr(self.building, 'recent_annual_fossil_fuel_kWh')):
            html_txt += '    <td class="td_border" colspan="4">' + '{:,}'.format(self.building.recent_annual_fossil_fuel_kWh) + '</td>'
        else:
            html_txt += '    <td class="td_border" colspan="4">No fossil fuel data</td>'
        html_txt += '  </tr>'
        html_txt += '  <tr>'
        html_txt += '    <td class="td_border" colspan="4"><b>Annual Cost (' + self.currency_str + ')</b></td>'
        if(hasattr(self.building, 'recent_annual_electricity_cost')):
            html_txt += '    <td class="td_border"  colspan="4">' + '{:,}'.format(self.building.recent_annual_electricity_cost) + '</td>'
        else:
            html_txt += '    <td class="td_border"  colspan="4">No electricity data</td>'
        #  html_txt += '    <td class="td_border" colspan="4"><b>Annual  Cost (' + self.currency_str + ')</b></td>'
        if(hasattr(self.building, 'recent_annual_fossil_fuel_cost')):
            html_txt += '    <td class="td_border"  colspan="4">' + '{:,}'.format(self.building.recent_annual_fossil_fuel_cost) + '</td>'
        else:
            html_txt += '    <td class="td_border"  colspan="4">No fossil fuel data</td>'
        html_txt += '  </tr>'
        html_txt += '  <tr>'
        html_txt += '    <td class="td_border" colspan="4"><b>Annual Site EUI (kWh/m<sup>2</sup>)</b></td>'
        if(hasattr(self.building, 'recent_annual_electricity_EUI')):
            html_txt += '    <td class="td_border" colspan="4">' + '{:,}'.format(self.building.recent_annual_electricity_EUI) + '</td>'
        else:
            html_txt += '    <td class="td_border" colspan="4">No electricity data</td>'
        #  html_txt += '    <td class="td_border" colspan="4"><b>Annual Site EUI (kWh/m<sup>2</sup>)</b></td>'
        if(hasattr(self.building,'recent_annual_fossil_fuel_EUI')):
            html_txt += '    <td class="td_border" colspan="4">' + '{:,}'.format(self.building.recent_annual_fossil_fuel_EUI) + '</td>'
        else:
            html_txt += '    <td class="td_border" colspan="4">No fossil fuel data</td>'
        html_txt += '  </tr>'
        html_txt += '    </table>'

        html_txt += '<p style="margin:0px;">&nbsp;&nbsp;<i>Note: The annual results are from the most recent 12 months\' input.</i></p>'
        html_txt += '</div>'
        html_txt += '</div>'


        ### Saving Potentials Card
        html_txt += '<br>'
        html_txt += '  <div class="w3-container w3-padding-large w3-white">'
        html_txt += '    <h2 id="about"><b>Saving Potentials</b></h2>'
        html_txt += '    <hr class="w3-opacity">'

        html_txt += '<div class="w3-container w3-margin-bottom w3-col m12 w3-padding-small">'
        html_txt += '<div class="w3-container ">'
        # Savings plots start
        # Savings plot row 1 -- saving numbers and target
        html_txt += '<div class="w3-cell-row">'

        # Col 1 -- Saving numbers
        html_txt += '<div class="w3-container w3-cell w3-hover-indigo w3-mobile">'
        html_txt += '<p class="w3-xlarge">    Target Selection: <b>' + self.building.saving_target_str + '</b></p>'
        html_txt += '<p class="w3-xlarge">    Potential Cost Savings: </p><p class="number">' + self.currency_str + " {:,}".format(
            int(self.building.total_cost_savings)) + '</p>'
        html_txt += '<p class="w3-xlarge">    Potential Percent Savings: </p><p class = "number">' + "{:,}".format(
            self.building.total_energy_savings_pct) + '%</p>'
        html_txt += '</div>'
        
        # Col 2 -- EE recommendations
        html_txt += '<div class="w3-container w3-hover-indigo w3-cell w3-mobile">'
        html_txt += '<h5><b>Energy Efficiency Recommendations</b></h5>'
        html_txt += '<ul>'
        for i in range(len(self.building.FIM_list)):
            html_txt += '<li>' + self.building.FIM_list[i] + '</li>'
        html_txt += '</ul>'
        html_txt += '<a href="#EE" onclick="w3_close()" class="w3-bar-item w3-button w3-padding"><i class="fa fa-th-large fa-info w3-margin-right"></i>Details</a> '
        html_txt += '</div>'
        html_txt += '</div><hr>'
        # Savings plot row 2 -- stacked bar chart and pie chart
        html_txt += '''
                <div class="w3-row">
                    <div class="w3-half">
                    <p  class="w3-center"> <b> Utility Cost Breakdown (Thousands'''+ self.currency_str +''') </b> </p>
                        <canvas id="disag" style="height:500px"></canvas>
                    </div>
                    <div  class="w3-half">
                    <p  class="w3-center"><b> Utility Cost Savings ('''+ self.currency_str +''') </b></p>
                        <canvas id="saving_pie_chart" style="height:500px"></canvas>
                    </div>
                </div>'''
        html_txt += self.saving_bar_str
        html_txt += self.saving_pie_str
        html_txt += '<div class="w3-container w3-content">'
        html_txt += '<hr><button class="w3-button w3-border w3-hover-grey" onclick="showTrends()">Show/Hide original and predicted consumption with upgrade</button>'
        html_txt += '</div>'
        # Savings plot row 3 -- hidden saving trend charts
        html_txt += '<div class="w3-cell-row" id="trend_plot" style = "display:none">'
        # html_txt += '<div class="w3-container w3-cell w3-mobile">'
        html_txt += '''
            <div id="trend_plot" class = "w3-row-padding">
                    <div class ="w3-half">
                        <canvas id="consumption_e"></canvas>
                    </div>
                    <div class="w3-half">
                        <canvas id="consumption_f"></canvas>
                    </div>
            </div>'''
        if(hasattr(self.building, 'energy_savings_fig_e')):
            html_txt += '<div id="trend_plot" class = "w3-row-padding">'
            html_txt += self.building.energy_savings_fig_e
        else:
            html_txt += '<p>No electricity data</p>'
        if(hasattr(self.building, 'energy_savings_fig_f')):
            html_txt += self.building.energy_savings_fig_f
        else:
            html_txt += '<p>No fossil fuel data</p>'
        html_txt += '</div>'
        html_txt += '</div>'
        # Savings plots end
        html_txt += '</div>'

        # EE recommendations brief
        html_txt += '<div class="w3-container w3-margin-bottom w3-padding-small">'
        html_txt += '</div>'
        html_txt += '</div>'
        html_txt += '<br>'

        ### Weather Sensitivity and Benchmarks Card
        html_txt += '  <div class="w3-container w3-padding-large w3-white" id="about">'
        html_txt += '    <h2 id="benchmark"><b>Weather Sensitivity and Benchmarks</b></h2>'
        html_txt += '    <hr class="w3-opacity">'
        html_txt += "Daily electricity and fossil fuel  use per floor area is plotted below against monthly average outdoor air temperature. When energy use goes up at low temperatures on the left side of the graph, it represents heating energy. When energy use goes up at high temperatures on the right side of the graph, it represents cooling energy. The flat part of the graph shows the building's base load."
        html_txt += '    <hr>'

        # Electricity model and benchmarking
        html_txt += '<div class="w3-row">'
        if(hasattr(self.building,'im_electricity') and hasattr(self.building.im_electricity, 'model_description_html')):
            html_txt += self.building.im_electricity.model_description_html
        html_txt += '</div>'
        html_txt += '<div class="w3-row">'
        html_txt += '  <div class="w3-half w3-container w3-margin-bottom w3-col m5 w3-padding-small">'
        html_txt += '    <div class="w3-container ">'
        html_txt += '      <p><b>Electricity Change-point Model</b></p>'
        if (hasattr(self.building, 'im_electricity') and hasattr(self.building.im_electricity, 'model_description_html')):
            # html_txt += self.building.im_electricity.fig_html)
            html_txt += '<div class="graph_container"> '
            html_txt += '<canvas id="e_model" style="height:240px;"></canvas>'
            html_txt += '</div>'
            html_txt += self.building.im_electricity.model_chart_html

        else:
            html_txt += '<p>No electricity consumption data is provided or no significant change-point model for electricity was found.</p>'
        html_txt += '    </div>'
        html_txt += '  </div>'
        html_txt += '<div class="w3-half w3-container w3-margin-bottom w3-col m7 w3-padding-small">'
        #html_txt += '<div class="w3-container ">'
        html_txt += '<p><b>Electricity Consumption Benchmarking</b></p>'
        html_txt += self.building.benchmarking_bar_base_e_html
        html_txt += self.building.benchmarking_bar_hsl_e_html
        html_txt += self.building.benchmarking_bar_hcp_e_html
        html_txt += self.building.benchmarking_bar_csl_e_html
        html_txt += self.building.benchmarking_bar_ccp_e_html
        html_txt += '<p><i>Note: % indicate the percentage of buildings your building is superior to.</i></p>'
        html_txt += '<a href="#IMT" onclick="w3_close()" class="w3-bar-item w3-button w3-padding"><i class="fa fa-th-large fa-info w3-margin-right"></i>Details</a> '
        html_txt += '</div>'
        html_txt += '</div>'
        # -->Electricity model and benchmarking end

        html_txt += '<hr>'
        # Fossil fuel model and benchmarking
        html_txt += '<div class="w3-row">'
        if (hasattr(self.building, 'im_fossil_fuel') and hasattr(self.building.im_fossil_fuel, 'model_description_html')):
            html_txt += self.building.im_fossil_fuel.model_description_html
        html_txt += '</div>'
        html_txt += '<div class="w3-row">'
        html_txt += '  <div class="w3-half w3-container w3-margin-bottom w3-col m5 w3-padding-small">'
        html_txt += '    <div class="w3-container">'
        html_txt += '      <p><b>Fossil Fuel Change-point Model</b></p>'
        if (hasattr(self.building, 'im_fossil_fuel') and hasattr(self.building.im_fossil_fuel, 'model_description_html')):
            #html_txt += self.building.im_fossil_fuel.fig_html
            html_txt += '<div class="graph_container"> '
            html_txt += '<canvas id="f_model" style="height:240px;"></canvas>'
            html_txt += '</div>'
            html_txt += self.building.im_fossil_fuel.model_chart_html

        else:
            html_txt += '<p>No fossil fuel consumption data is provided or no significant change-point model for fossil fuel was found.</p>'
        html_txt += '    </div>'
        html_txt += '  </div>    '
        html_txt += '<div class="w3-half w3-container w3-margin-bottom w3-col m7 w3-padding-small">'
        html_txt += '<div class="w3-container">'
        html_txt += '<p><b>Fossil Fuel Consumption Benchmarking</b></p>'
        html_txt += self.building.benchmarking_bar_base_f_html
        html_txt += self.building.benchmarking_bar_hsl_f_html
        html_txt += self.building.benchmarking_bar_hcp_f_html
        html_txt += self.building.benchmarking_bar_csl_f_html
        html_txt += self.building.benchmarking_bar_ccp_f_html
        html_txt += '<p><i>Note: % indicate the percentage of buildings your building is superior to.</i></p>'
        html_txt += '<a href="#IMT" onclick="w3_close()" class="w3-bar-item w3-button w3-padding"><i class="fa fa-th-large fa-info w3-margin-right"></i>Details</a> '
        html_txt += '</div>'
        html_txt += '</div>'
        html_txt += '</div>'
        # -->Fossil fuel model and benchmarking end

        html_txt += '</div>'
        html_txt += '  <br>'

        # Detail EE analysis
        html_txt += '  <div class="w3-container w3-padding-large w3-white">'
        html_txt += '    <h2 id="EE"><b>Energy Efficiency Measure Recommendations</b></h2>'
        html_txt += '    <p>More details on each energy efficiency opportunity identified </p>'
        FIM_des = {
            "Reduce Equipment Schedules": "Your building equipment load is higher than typical. Equipment and systems within any building should operate using a schedule. Check equipment schedule and if equipment is operational during low occupancy times or during reduced building use. Setup a notification to identify when schedules are overridden and are not returned to normal.",
            "Reduce Lighting Load": "Your building lighting load is higher than typical. Lighting load is an ample portion of any building energy consumption. Lighting efficiency and controls have big impact on lighting system performance. Consider upgrading bulbs and fixtures to improve efficiency and check existing (or upgrade to) controls that dim and turn off the lights appropriately. Take advantage of natural daylighting whenever possible. Lights near existing window or skylights can be controlled to dim or turn off for maximum daylight utilization. Renovations to the building envelope and internal space configurations are good opportunity to check lighting system performance. ",
            "Reduce Plug Loads": " Your building plug load is higher than typical. Anything that is plugged into standard electric receptacles or outlets fall under plug load. Personal computers, monitors, printers, coffeemakers, other office/lab/lighting equipment are examples of plug loads. Consider upgrading to more efficient models and operate on a schedule where possible.",
            "Increase Cooling System Efficiency": "Your building cooling load is higher than similar buildings for similar weather conditions. HVAC system performance has big impact on building energy consumption. Check your cooling system, all related equipment and controls to improve system efficiency. Upgrading your system to a more efficient model, will reduce your system energy consumption.",
            "Decrease Heating Setpoints": "Your building heating setpoint is higher than typical buildings. Check the occupied and unoccupied heating setpoint during the heating season. Heating system and auxiliaries’ energy consumption will be reduced by decreasing the heating setpoint.",
            "Ensure Adequate Ventilation Rate": "Correct percentage of fresh air into the building is necessary to provide comfortable and safe conditions for building occupants. Reducing the amount of fresh air will reduce the energy used to condition and distribute it. Make sure to understand and follow all related building codes.",
            "Decrease Infiltration": "Infiltration is the uncontrolled outside air that is brought into a building. It adds to the overall building cooling and heating loads. Infiltration is reduced with caulking, weather stripping, and upgrades in envelope components (e.g. windows, doors, air intakes and exhausts).",
            "Increase Heating System Efficiency": "Your building heating load is higher than similar buildings for similar weather conditions. HVAC system performance has big impact on building energy consumption. Check the heating system, related equipment and controls for efficient operations. Upgrading your system to a more efficient model, will reduce your system energy consumption.",
            "Add Wall/Ceiling Insulation": "Heating and cooling loads are reduced by insulating the building walls, ceilings, and foundations. Check current insulation levels and assess opportunities of adding more insulation.",
            "Check Fossil Baseload": "Your building thermal load is higher than typical. Check building thermal baseload (minimum continuous usage) for the building. Poor operating schedules, simultaneous heating and cooling, and faulty heating equipment result in higher baseload.",
            "Upgrade Windows": "Windows have big impact on heating and cooling loads. Poor window insulation is like low insulation wall. Check current windows for U-value.",
            "Eliminate Electric Heating": "Your building electric heating load is higher than typical. Electric heating is expensive and increases heating system energy consumption. Check electric heating system schedules and controls. ",
            "Increase Cooling Setpoints" : "Your building starts cooling at lower temperature than typical. Check the occupied and unoccupied cooling setpoint during the cooling season. Cooling system and auxiliaries’ energy consumption will be reduced by increasing the cooling setpoint ",
            "Add/Fix Economizers":"Utilizing outside air that is cooler and/or drier than indoor air in an economizer can significantly reduce the energy used to cool the building. Check existing economizers, if any, for efficient operations."

        }
        for i in range(len(self.building.FIM_list)):
            html_txt += '<h4>' + self.building.FIM_list[i] + '</h4>'
            html_txt += '<p>' + FIM_des[self.building.FIM_list[i]] + '</p>'
        if not self.building.FIM_list:
            html_txt += '<p>No recommendation is available.</p>'

        # html_txt += '<p><i>Note: Special thanks to Johnson Controls (JCI) technical team for their valuable technical support and for their algorithm in identifying Energy Efficiency Recommendations.</i></p>'
        html_txt += '    <hr class="w3-opacity">'
        html_txt += '  </div>'
        html_txt += '  <br>'

        html_txt += '  <div class="w3-container w3-padding-large w3-white">'
        html_txt += '    <h2 id="IMT"><b>Understand the Model</b></h2>'
        html_txt += """
            <h4>Baseload</h4>
            <p>Energy consumption of all non-weather-related equipment like computers and lighting. The lower the baseload, the less the energy consumed in plugs and permanently plugged equipment.</p>

            <h4>Cooling Sensitivity </h4>
            <p>Cooling system energy consumption for each degree increase in outdoor temperature. Low cooling sensitivity results in less energy-consuming cooling system.</p>

            <h4>Cooling change-point</h4>
            <p>The temperature at which cooling system starts. Below the cooling change point, the cooling system is not operational.</p>

            <h4>Heating Sensitivity</h4>
            <p>Heating system consumption of energy for each degree decrease in outdoor temperature. Low heating sensitivity results in less energy-consuming heating system.</p>

            <h4>Heating change-point</h4>
            <p>The temperature at which heating system starts. Above the heating change point, the cooling system is not operational.</p>
                        """
        html_txt += '    <hr class="w3-opacity">'
        html_txt += '  </div>'
        html_txt += '  <br>'

        # Tool description
        # html_txt += '  <div class="w3-container w3-padding-large w3-white">'
        # html_txt += '    <h2 id="About"><b>What is BETTER?</b></h2>'
        # html_txt += "  <p>The Building Efficiency Targeting Tool for Energy Retrofits (BETTER) helps building owners and managers quickly assess potential opportunities for energy savings, to inform decisions on where to target energy efficiency efforts. The tool can identify low and no-cost opportunities that can be implemented immediately, as well as retrofit opportunities that can be investigated further through more detailed audits or studies.</p>"
        # html_txt += "  <p>The tool uses regression techniques to analyze a building's monthly energy data and weather, in order to determine how much energy is used for heating, cooling, and baseload (lighting, plug loads, etc.). The performance of the building is then benchmarked against similar building. In addition to telling you whether a building's energy consumption is higher or lower than peers, it goes a step further to tell you why that is the case. If a building's energy use is high compared to peers, for example, it can tell you it is because the heating system is performing poorly, while the cooling system and baseload equipment are typical compared to peers. With this information, a building owner can adjust heating setpoints, add insulation, or perform an energy audit that focuses on heating equipment.</p>"

        # html_txt += '    <hr class="w3-opacity">'
        # html_txt += '  </div>'
        # html_txt += '  <br>'

        html_txt += '  <!-- Footer -->'
        html_txt += '  <footer class="w3-container w3-padding-32 w3-white">'
        html_txt += '  <div class="w3-row-padding">'
        html_txt += '    <div class="w3-half">'
        # html_txt += '      <h3>Partners</h3>'
        # html_txt += '      <p>Place holder.</p>'
        html_txt += self.equans_logo
        html_txt += '<br>'
        html_txt += 'A Bouygues Group Company'
        html_txt += '    </div>'
        # html_txt += '    <div class="w3-half">'
        # html_txt += '      <h3>Links</h3>'
        # html_txt += '      <ul class="w3-ul w3-hoverable">'
        # html_txt += '        <li class="w3-padding-16">'
        # html_txt += '          <span class="w3-large"><a href="https://github.com/LBNL-JCI-ICF/better">GitHub Repository</a></span><br>'
        # html_txt += '        </li>'
        # html_txt += '      </ul>'
        # html_txt += '    </div>'
        html_txt += '  </div>'
        html_txt += '  </footer>'

        html_txt += '  <div class="w3-black w3-center w3-padding-24"></div>'
        html_txt += '</div>'

        ######inline javascript#####
        # html_txt += '<script>'
        # html_txt += 'function w3_open() {'
        # html_txt += '    document.getElementById("mySidebar").style.display = "block";'
        # html_txt += '    document.getElementById("myOverlay").style.display = "block";'
        # html_txt += '}'
        # html_txt += 'function w3_close() {'
        # html_txt += '    document.getElementById("mySidebar").style.display = "none";'
        # html_txt += '    document.getElementById("myOverlay").style.display = "none";'
        # html_txt += '}'

        # Show/hide trends
        # html_txt += 'function showTrends() {'
        # html_txt += '    var x = document.getElementById("trend_plot");'
        # html_txt += '    if (x.style.display === "none") {'
        # html_txt += '        x.style.display = "block";'
        # html_txt += '    } else {'
        # html_txt += '        x.style.display = "none";'
        # html_txt += '    }'
        # html_txt += '}'

        # html_txt += '</script>'
        return html_txt

    def generate_building_report_beta(self, report_path):
        report_file = os.path.join(
            report_path,
            str(self.building.bldg_id) + '_' + self.building.bldg_address + '_' + self.building.bldg_name + '_report.html'
        )
        report_file = report_file.replace(' ', '_')
        print(report_file)
        with open(report_file, 'w', encoding="utf-8") as report_html:
            report_html.write('<!DOCTYPE html>')
            report_html.write('<html>')
            report_html.write('<title>Building Efficiency Targeting Tool for Energy Retrofits (BETTER) Report</title>')

            # Add basic stuff including css and scripts
            report_html.write(self.html_basic())

            report_html.write('<body class="w3-light-grey w3-content" style="max-width:1500px">')
            report_html.write('<!-- Sidebar/menu -->')

             # Navigation bar
            report_html.write(self.navigation_bar())

            # Building Overview Card
            report_html.write('  <div class="w3-container w3-padding-large w3-white">')
            report_html.write('    <h2 id="overview"><b>' + self.building.bldg_name.upper() + '</b></h2>')
            report_html.write('    <hr class="w3-opacity">')

            report_html.write('<div class="w3-container w3-margin-bottom w3-padding-small">')
            report_html.write('    <table class="w3-table w3-bordered w3-border" style="width:95% border: solid 1 px blue">')
            report_html.write('  <tr>')
            report_html.write('    <td class="td_border" colspan="3"><b>Building Type</b></td>')
            report_html.write('    <td class="td_border" colspan="3">' + self.building.bldg_type + '</td>')
            report_html.write('    <td class="td_border" colspan="3"><b>Building Location</b></td>')
            report_html.write('    <td class="td_border" colspan="3">' + self.building.bldg_address + '</td>')
            report_html.write('  </tr>')
            report_html.write('  <tr>')
            report_html.write('    <td class="td_border" colspan="3"><b>Gross Floor Area (m<sup>2</sup>)</b></td>')
            report_html.write('    <td class="td_border" colspan="9">' + '{:,}'.format(self.building.bldg_area) + '</td>')
            report_html.write('  </tr>')
            report_html.write('  </table>')
            report_html.write('  <br>')
            report_html.write('    <table class="w3-table w3-bordered w3-border" style="width:95% border: solid 1 px blue">')
            report_html.write('  <tr>')
            report_html.write('    <td class="td_border" colspan="4"></td>')
            report_html.write('    <td class="td_border" colspan="4"><b>Electricity</b></td>')
            report_html.write('    <td class="td_border" colspan="4"><b>Fossil Fuel</b></td>')
            report_html.write('  </tr>')
            report_html.write('  <tr>')
            report_html.write('    <td class="td_border" colspan="4"><b>Annual Consumption (kWh)</b></td>')
            if(hasattr(self.building, 'recent_annual_electricity_kWh')):
                report_html.write('    <td class="td_border" colspan="4">' + '{:,}'.format(self.building.recent_annual_electricity_kWh) + '</td>')
            else:
                report_html.write('    <td class="td_border" colspan="4">No electricity data</td>')
          #  report_html.write('    <td class="td_border" colspan="4"><b>Annual Fossil Fuel Consumption (kWh)</b></td>')
            if(hasattr(self.building, 'recent_annual_fossil_fuel_kWh')):
                report_html.write('    <td class="td_border" colspan="4">' + '{:,}'.format(self.building.recent_annual_fossil_fuel_kWh) + '</td>')
            else:
                report_html.write('    <td class="td_border" colspan="4">No fossil fuel data</td>')
            report_html.write('  </tr>')
            report_html.write('  <tr>')
            report_html.write('    <td class="td_border" colspan="4"><b>Annual Cost (' + self.currency_str + ')</b></td>')
            if(hasattr(self.building, 'recent_annual_electricity_cost')):
                report_html.write('    <td class="td_border"  colspan="4">' + '{:,}'.format(self.building.recent_annual_electricity_cost) + '</td>')
            else:
                report_html.write('    <td class="td_border"  colspan="4">No electricity data</td>')
          #  report_html.write('    <td class="td_border" colspan="4"><b>Annual  Cost (' + self.currency_str + ')</b></td>')
            if(hasattr(self.building, 'recent_annual_fossil_fuel_cost')):
                report_html.write('    <td class="td_border"  colspan="4">' + '{:,}'.format(self.building.recent_annual_fossil_fuel_cost) + '</td>')
            else:
                report_html.write('    <td class="td_border"  colspan="4">No fossil fuel data</td>')
            report_html.write('  </tr>')
            report_html.write('  <tr>')
            report_html.write('    <td class="td_border" colspan="4"><b>Annual Site EUI (kWh/m<sup>2</sup>)</b></td>')
            if(hasattr(self.building, 'recent_annual_electricity_EUI')):
                report_html.write('    <td class="td_border" colspan="4">' + '{:,}'.format(self.building.recent_annual_electricity_EUI) + '</td>')
            else:
                report_html.write('    <td class="td_border" colspan="4">No electricity data</td>')
          #  report_html.write('    <td class="td_border" colspan="4"><b>Annual Site EUI (kWh/m<sup>2</sup>)</b></td>')
            if(hasattr(self.building,'recent_annual_fossil_fuel_EUI')):
                report_html.write('    <td class="td_border" colspan="4">' + '{:,}'.format(self.building.recent_annual_fossil_fuel_EUI) + '</td>')
            else:
                report_html.write('    <td class="td_border" colspan="4">No fossil fuel data</td>')
            report_html.write('  </tr>')
            report_html.write('    </table>')
            report_html.write('<p style="margin:0px;">&nbsp;&nbsp;<i>Note: The annual results are from the most recent 12 months\' input.</i></p>')
            report_html.write('</div>')
            report_html.write('</div>')


            ### Saving Potentials Card
            report_html.write('<br>')
            report_html.write('  <div class="w3-container w3-padding-large w3-white">')
            report_html.write('    <h2 id="about"><b>Saving Potentials</b></h2>')
            report_html.write('    <hr class="w3-opacity">')

            report_html.write('<div class="w3-container w3-margin-bottom w3-col m12 w3-padding-small">')
            report_html.write('<div class="w3-container ">')
            # Savings plots start
            # Savings plot row 1 -- saving numbers and target
            report_html.write('<div class="w3-cell-row">')
            # Col 1 -- Saving numbers
            report_html.write('<div class="w3-container w3-cell w3-hover-indigo w3-mobile">')
            report_html.write('<p class="w3-xlarge">    Target Selection: ' + self.building.saving_target_str + '</p>')
            report_html.write('<p class="w3-xlarge">    Potential Cost Savings: </p><p class="number">' + self.currency_str + " {:,}".format(
                int(self.building.total_cost_savings)) + '</p>')
            report_html.write('<p class="w3-xlarge">    Potential Percent Savings: </p><p class = "number">' + "{:,}".format(
                self.building.total_energy_savings_pct) + '%</p>')
            report_html.write('</div>')
            # Col 2 -- EE recommendations
            report_html.write('<div class="w3-container w3-hover-indigo w3-cell w3-mobile">')
            report_html.write('<h5><b>Energy Efficiency Recommendations</b></h5>')
            report_html.write('<ul>')
            for i in range(len(self.building.FIM_list)):
                report_html.write('<li>' + self.building.FIM_list[i] + '</li>')
            report_html.write('</ul>')
            report_html.write(
                '<a href="#EE" onclick="w3_close()" class="w3-bar-item w3-button w3-padding"><i class="fa fa-th-large fa-info w3-margin-right"></i>Details</a> ')
            report_html.write('</div>')
            report_html.write('</div><hr>')
            # Savings plot row 2 -- stacked bar chart and pie chart
            report_html.write('''
                  <div class="w3-row">
                      <div class="w3-half">
                      <p  class="w3-center"> <b> Utility Cost Breakdown (Thousands'''+ self.currency_str +''') </b> </p>
                          <canvas id="disag" style="height:500px"></canvas>
                      </div>
                      <div  class="w3-half">
                      <p  class="w3-center"><b> Utility Cost Savings ('''+ self.currency_str +''') </b></p>
                          <canvas id="saving_pie_chart" style="height:500px"></canvas>
                      </div>
                  </div>''')
            report_html.write(self.saving_bar_str)
            report_html.write(self.saving_pie_str)
            report_html.write('<div class="w3-container w3-content">')
            report_html.write('<hr><button class="w3-button w3-border w3-hover-grey" onclick="showTrends()">Show/Hide original and predicted consumption with upgrade</button>')
            report_html.write('</div>')
            # Savings plot row 3 -- hidden saving trend charts
            report_html.write('<div class="w3-cell-row" id="trend_plot" style = "display:none">')
            #report_html.write('<div class="w3-container w3-cell w3-mobile">')
            report_html.write('''
                <div id="trend_plot" class = "w3-row-padding">
                      <div class ="w3-half">
                            <canvas id="consumption_e"></canvas>
                      </div>
                      <div class="w3-half">
                            <canvas id="consumption_f"></canvas>
                      </div>
                </div>''')
            if(hasattr(self.building, 'energy_savings_fig_e')):
                report_html.write(self.building.energy_savings_fig_e)
            else:
                report_html.write('<p>No electricity data</p>')
            if(hasattr(self.building, 'energy_savings_fig_f')):
                report_html.write(self.building.energy_savings_fig_f)
            else:
                report_html.write('<p>No fossil fuel data</p>')
            report_html.write('</div>')
            report_html.write('</div>')
            # Savings plots end
            report_html.write('</div>')
            # EE recommendations brief
            report_html.write('<div class="w3-container w3-margin-bottom w3-padding-small">')
            report_html.write('</div>')
            report_html.write('</div>')
            report_html.write('<br>')


            ### Weather Sensitivity and Benchmarks Card
            report_html.write('  <div class="w3-container w3-padding-large w3-white" id="about">')
            report_html.write('    <h2 id="benchmark"><b>Weather Sensitivity and Benchmarks</b></h2>')
            report_html.write('    <hr class="w3-opacity">')
            report_html.write(
                "Daily electricity and fossil fuel  use per floor area is plotted below against monthly average outdoor air temperature. When energy use goes up at low temperatures on the left side of the graph, it represents heating energy. When energy use goes up at high temperatures on the right side of the graph, it represents cooling energy. The flat part of the graph shows the building's base load.")
            report_html.write('    <hr>')

            # Electricity model and benchmarking
            report_html.write('<div class="w3-row">')
            if(hasattr(self.building,'im_electricity') and hasattr(self.building.im_electricity, 'model_description_html')):
                report_html.write(self.building.im_electricity.model_description_html)
            report_html.write('</div>')
            report_html.write('<div class="w3-row">')
            report_html.write('  <div class="w3-half w3-container w3-margin-bottom w3-col m5 w3-padding-small">')
            report_html.write('    <div class="w3-container ">')
            report_html.write('      <p><b>Electricity Change-point Model</b></p>')
            if (hasattr(self.building, 'im_electricity') and hasattr(self.building.im_electricity, 'model_description_html')):
                # report_html.write(self.building.im_electricity.fig_html)
                report_html.write('<div class="graph_container"> ')
                report_html.write('<canvas id="e_model" style="height:240px;"></canvas>')
                report_html.write('</div>')
                report_html.write(self.building.im_electricity.model_chart_html)

            else:
                report_html.write(
                    '<p>No electricity consumption data is provided or no significant change-point model for electricity was found.</p>')
            report_html.write('    </div>')
            report_html.write('  </div>')
            report_html.write('<div class="w3-half w3-container w3-margin-bottom w3-col m7 w3-padding-small">')
            #report_html.write('<div class="w3-container ">')
            report_html.write('<p><b>Electricity Consumption Benchmarking</b></p>')
            report_html.write(self.building.benchmarking_bar_base_e_html)
            report_html.write(self.building.benchmarking_bar_hsl_e_html)
            report_html.write(self.building.benchmarking_bar_hcp_e_html)
            report_html.write(self.building.benchmarking_bar_csl_e_html)
            report_html.write(self.building.benchmarking_bar_ccp_e_html)
            report_html.write('<p><i>Note: % indicate the percentage of buildings your building is superior to.</i></p>')
            report_html.write(
                 '<a href="#IMT" onclick="w3_close()" class="w3-bar-item w3-button w3-padding"><i class="fa fa-th-large fa-info w3-margin-right"></i>Details</a> ')
            report_html.write('</div>')
            report_html.write('</div>')
            # -->Electricity model and benchmarking end

            report_html.write('<hr>')
            # Fossil fuel model and benchmarking
            report_html.write('<div class="w3-row">')
            if (hasattr(self.building, 'im_fossil_fuel') and hasattr(self.building.im_fossil_fuel, 'model_description_html')):
                report_html.write(self.building.im_fossil_fuel.model_description_html)
            report_html.write('</div>')
            report_html.write('<div class="w3-row">')
            report_html.write('  <div class="w3-half w3-container w3-margin-bottom w3-col m5 w3-padding-small">')
            report_html.write('    <div class="w3-container">')
            report_html.write('      <p><b>Fossil Fuel Change-point Model</b></p>')
            if (hasattr(self.building, 'im_fossil_fuel') and hasattr(self.building.im_fossil_fuel, 'model_description_html')):
                #report_html.write(self.building.im_fossil_fuel.fig_html)
                report_html.write('<div class="graph_container"> ')
                report_html.write('<canvas id="f_model" style="height:240px;"></canvas>')
                report_html.write('</div>')
                report_html.write(self.building.im_fossil_fuel.model_chart_html)

            else:
                report_html.write(
                    '<p>No fossil fuel consumption data is provided or no significant change-point model for fossil fuel was found.</p>')
            report_html.write('    </div>')
            report_html.write('  </div>    ')
            report_html.write('<div class="w3-half w3-container w3-margin-bottom w3-col m7 w3-padding-small">')
            report_html.write('<div class="w3-container">')
            report_html.write('<p><b>Fossil Fuel Consumption Benchmarking</b></p>')
            report_html.write(self.building.benchmarking_bar_base_f_html)
            report_html.write(self.building.benchmarking_bar_hsl_f_html)
            report_html.write(self.building.benchmarking_bar_hcp_f_html)
            report_html.write(self.building.benchmarking_bar_csl_f_html)
            report_html.write(self.building.benchmarking_bar_ccp_f_html)
            report_html.write('<p><i>Note: % indicate the percentage of buildings your building is superior to.</i></p>')
            report_html.write(
                 '<a href="#IMT" onclick="w3_close()" class="w3-bar-item w3-button w3-padding"><i class="fa fa-th-large fa-info w3-margin-right"></i>Details</a> ')
            report_html.write('</div>')
            report_html.write('</div>')
            report_html.write('</div>')
            # -->Fossil fuel model and benchmarking end

            report_html.write('</div>')
            report_html.write('  <br>')

            # Detail EE analysis
            report_html.write('  <div class="w3-container w3-padding-large w3-white">')
            report_html.write('    <h2 id="EE"><b>Energy Efficiency Recommendation Details</b></h2>')
            report_html.write('    <p>More details on each energy efficiency opportunity identified </p>')
            FIM_des = {
                "Reduce Equipment Schedules": "Your building equipment load is higher than typical. Equipment and systems within any building should operate using a schedule. Check equipment schedule and if equipment is operational during low occupancy times or during reduced building use. Setup a notification to identify when schedules are overridden and are not returned to normal.",
                "Reduce Lighting Load": "Your building lighting load is higher than typical. Lighting load is an ample portion of any building energy consumption. Lighting efficiency and controls have big impact on lighting system performance. Consider upgrading bulbs and fixtures to improve efficiency and check existing (or upgrade to) controls that dim and turn off the lights appropriately. Take advantage of natural daylighting whenever possible. Lights near existing window or skylights can be controlled to dim or turn off for maximum daylight utilization. Renovations to the building envelope and internal space configurations are good opportunity to check lighting system performance. ",
                "Reduce Plug Loads": " Your building plug load is higher than typical. Anything that is plugged into standard electric receptacles or outlets fall under plug load. Personal computers, monitors, printers, coffeemakers, other office/lab/lighting equipment are examples of plug loads. Consider upgrading to more efficient models and operate on a schedule where possible.",
                "Increase Cooling System Efficiency": "Your building cooling load is higher than similar buildings for similar weather conditions. HVAC system performance has big impact on building energy consumption. Check your cooling system, all related equipment and controls to improve system efficiency. Upgrading your system to a more efficient model, will reduce your system energy consumption.",
                "Decrease Heating Setpoints": "Your building heating setpoint is higher than typical buildings. Check the occupied and unoccupied heating setpoint during the heating season. Heating system and auxiliaries’ energy consumption will be reduced by decreasing the heating setpoint.",
                "Ensure Adequate Ventilation Rate": "Correct percentage of fresh air into the building is necessary to provide comfortable and safe conditions for building occupants. Reducing the amount of fresh air will reduce the energy used to condition and distribute it. Make sure to understand and follow all related building codes.",
                "Decrease Infiltration": "Infiltration is the uncontrolled outside air that is brought into a building. It adds to the overall building cooling and heating loads. Infiltration is reduced with caulking, weather stripping, and upgrades in envelope components (e.g. windows, doors, air intakes and exhausts).",
                "Increase Heating System Efficiency": "Your building heating load is higher than similar buildings for similar weather conditions. HVAC system performance has big impact on building energy consumption. Check the heating system, related equipment and controls for efficient operations. Upgrading your system to a more efficient model, will reduce your system energy consumption.",
                "Add Wall/Ceiling Insulation": "Heating and cooling loads are reduced by insulating the building walls, ceilings, and foundations. Check current insulation levels and assess opportunities of adding more insulation.",
                "Check Fossil Baseload": "Your building thermal load is higher than typical. Check building thermal baseload (minimum continuous usage) for the building. Poor operating schedules, simultaneous heating and cooling, and faulty heating equipment result in higher baseload.",
                "Upgrade Windows": "Windows have big impact on heating and cooling loads. Poor window insulation is like low insulation wall. Check current windows for U-value.",
                "Eliminate Electric Heating": "Your building electric heating load is higher than typical. Electric heating is expensive and increases heating system energy consumption. Check electric heating system schedules and controls. ",
                "Increase Cooling Setpoints" : "Your building starts cooling at lower temperature than typical. Check the occupied and unoccupied cooling setpoint during the cooling season. Cooling system and auxiliaries’ energy consumption will be reduced by increasing the cooling setpoint ",
                "Add/Fix Economizers":"Utilizing outside air that is cooler and/or drier than indoor air in an economizer can significantly reduce the energy used to cool the building. Check existing economizers, if any, for efficient operations."

            }
            for i in range(len(self.building.FIM_list)):
                report_html.write('<h4>' + self.building.FIM_list[i] + '</h4>')
                report_html.write('<p>' + FIM_des[self.building.FIM_list[i]] + '</p>')

            report_html.write('<p><i>Note: Special thanks to Johnson Controls (JCI) technical team for their valuable technical support and for their algorithm in identifying Energy Efficiency Recommendations.</i></p>')
            report_html.write('    <hr class="w3-opacity">')
            report_html.write('  </div>')
            report_html.write('  <br>')

            report_html.write('  <div class="w3-container w3-padding-large w3-white">')
            report_html.write('    <h2 id="IMT"><b>Understand the Model</b></h2>')
            report_html.write("""
                <h4>Baseload</h4>
                <p>Energy consumption of all non-weather-related equipment like computers and lighting. The lower the baseload, the less the energy consumed in plugs and permanently plugged equipment.</p>

                <h4>Cooling Sensitivity </h4>
                <p>Cooling system energy consumption for each degree increase in outdoor temperature. Low cooling sensitivity results in less energy-consuming cooling system.</p>

                <h4>Cooling change-point</h4>
                <p>The temperature at which cooling system starts. Below the cooling change point, the cooling system is not operational.</p>

                <h4>Heating Sensitivity</h4>
                <p>Heating system consumption of energy for each degree decrease in outdoor temperature. Low heating sensitivity results in less energy-consuming heating system.</p>

                <h4>Heating change-point</h4>
                <p>The temperature at which heating system starts. Above the heating change point, the cooling system is not operational.</p>
                           """)
            report_html.write('    <hr class="w3-opacity">')
            report_html.write('  </div>')
            report_html.write('  <br>')

            # Tool description
            report_html.write('  <div class="w3-container w3-padding-large w3-white">')
            report_html.write('    <h2 id="About"><b>What is BETTER?</b></h2>')
            report_html.write(
                "  <p>The Building Efficiency Targeting Tool for Energy Retrofits (BETTER) helps building owners and managers quickly assess potential opportunities for energy savings, to inform decisions on where to target energy efficiency efforts. The tool can identify low and no-cost opportunities that can be implemented immediately, as well as retrofit opportunities that can be investigated further through more detailed audits or studies.</p>")
            report_html.write(
                "  <p>The tool uses regression techniques to analyze a building's monthly energy data and weather, in order to determine how much energy is used for heating, cooling, and baseload (lighting, plug loads, etc.). The performance of the building is then benchmarked against similar building. In addition to telling you whether a building's energy consumption is higher or lower than peers, it goes a step further to tell you why that is the case. If a building's energy use is high compared to peers, for example, it can tell you it is because the heating system is performing poorly, while the cooling system and baseload equipment are typical compared to peers. With this information, a building owner can adjust heating setpoints, add insulation, or perform an energy audit that focuses on heating equipment.</p>")

            report_html.write('    <hr class="w3-opacity">')
            report_html.write('  </div>')
            report_html.write('  <br>')

            report_html.write('  <!-- Footer -->')
            report_html.write('  <footer class="w3-container w3-padding-32 w3-white">')
            report_html.write('  <div class="w3-row-padding">')
            report_html.write('    <div class="w3-half">')
            report_html.write('      <h3>Partners</h3>')
            # report_html.write('      <p>Place holder.</p>')
            report_html.write(self.equans_logo)
            report_html.write(self.icf_logo)
            report_html.write(self.jci_logo)
            report_html.write('    </div>')
            report_html.write('    <div class="w3-half">')
            report_html.write('      <h3>Links</h3>')
            report_html.write('      <ul class="w3-ul w3-hoverable">')
            report_html.write('        <li class="w3-padding-16">')
            report_html.write('          <span class="w3-large"><a href="https://github.com/LBNL-JCI-ICF/better">GitHub Repository</a></span><br>')
            report_html.write('        </li>')
            report_html.write('      </ul>')
            report_html.write('    </div>')
            report_html.write('  </div>')
            report_html.write('  </footer>')

            report_html.write('  <div class="w3-black w3-center w3-padding-24"></div>')
            report_html.write('</div>')
            report_html.write('<script>')
            report_html.write('function w3_open() {')
            report_html.write('    document.getElementById("mySidebar").style.display = "block";')
            report_html.write('    document.getElementById("myOverlay").style.display = "block";')
            report_html.write('}')
            report_html.write('function w3_close() {')
            report_html.write('    document.getElementById("mySidebar").style.display = "none";')
            report_html.write('    document.getElementById("myOverlay").style.display = "none";')
            report_html.write('}')

            # Show/hide trends
            report_html.write('function showTrends() {')
            report_html.write('    var x = document.getElementById("trend_plot");')
            report_html.write('    if (x.style.display === "none") {')
            report_html.write('        x.style.display = "block";')
            report_html.write('    } else {')
            report_html.write('        x.style.display = "none";')
            report_html.write('    }')
            report_html.write('}')

            report_html.write('</script>')
            report_html.write('</body>')
            report_html.write('</html>')
        return(report_file)

    def logo(self):
        self.cerc_logo = '<a href="https://cercbee.lbl.gov/"><img src="https://cercbee.lbl.gov/sites/default/files/styles/max_image/public/images/cerc_logo.jpg?itok=HE_BbWn3" style="height:220px;"></a>'
        self.lbl_logo = '<a href="https://www.lbl.gov/"><img src="https://creative.lbl.gov/wp-content/uploads/sites/23/2015/05/Berkeley_Lab_Logo_Large.png" style="height:100px;"></a>'
        self.icf_logo = '<a href="https://www.icf.com/"><img src="https://upload.wikimedia.org/wikipedia/commons/2/29/ICF_International_logo.png" style="height:100px;"></a>'
        self.jci_logo = '<a href="https://www.johnsoncontrols.com/"><img src="https://upload.wikimedia.org/wikipedia/en/thumb/0/0f/Johnson_Controls.svg/250px-Johnson_Controls.svg.png" style="height:100px;"></a>'
        self.equans_logo = '<a href="https://www.equans.be/"><img src="https://upload.wikimedia.org/wikipedia/fr/9/95/Logo-equans.jpg"></a>'


    def charts_js(self):
        # Horizontal bar chart
        self.saving_bar_str = '''
            <script>
                var barOptions_stacked = {
                    responsive: true,
                    legend: {
                    position: "bottom"
                    },

                    tooltips: {
                        enabled: true,
                        callbacks: {
                            label: function(tooltipItem, data) {
                                return Math.round(tooltipItem.xLabel).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")+" '''+ self.currency_str +'''"
                            },
                        }
                    },
                    hover :{
                        animationDuration:0
                    },
                    scales: {
                        xAxes: [{
                            ticks: {
                                callback: function (value) {
                                    return (value/1000.).toLocaleString()+" "
                                },
                                beginAtZero:true,
                                fontFamily: "sans-serif",
                                fontSize:16
                            },
                            scaleLabel:{
                                display:false
                            },
                            gridLines: {},
                            stacked: true
                        }],
                        yAxes: [{
                            gridLines: {
                                display:false,
                                color: "#fff",
                                zeroLineColor: "#fff",
                                zeroLineWidth: 1
                            },
                            ticks: {
                                fontFamily: "sans-serif",
                                fontSize:16
                            },
                            stacked: true
                        }],
                        legend:{
                            display:true
                        },
                        animation: {},
                        pointLabelFontFamily : "Quadon Extra Bold",
                        scaleFontFamily : "Quadon Extra Bold",
                    }}
                var ctx = document.getElementById("disag");
                var myChart = new Chart(ctx, {
                    type: 'horizontalBar',
                    data: {
                        labels: ["Your Building", "Typical Building", "Goal"],
                        datasets: [
                            {
                                label: "Cooling",
                                data: ['''+str(self.building.cooling_old_cost)+''', '''+str(self.building.cooling_typical_cost)+''', '''+str(self.building.cooling_new_cost)+'''],
                                backgroundColor: "rgba(31,78,121,1)",
                                hoverBackgroundColor: "rgba(21,68,111,1)"
                            },
                            {
                                label: "Baseload",
                                data: ['''+str(self.building.base_old_cost)+''', '''+str(self.building.base_typical_cost)+''', '''+str(self.building.base_new_cost)+'''],
                                backgroundColor: "rgba(127,127,127,1)",
                                hoverBackgroundColor: "rgba(117,117,117,1)"
                            },
                            {
                                label: "Heating",
                                data: ['''+str(self.building.heating_old_cost)+''', '''+str(self.building.heating_typical_cost)+''', '''+str(self.building.heating_new_cost)+'''],
                                backgroundColor: "rgba(192,0,0,1)",
                                hoverBackgroundColor: "rgba(182,0,0,1)"
                            }
                        ]
                    },
                    options: barOptions_stacked,
                });
            </script>
        '''

        self.saving_pie_str = '''
            <script>
                var ctx = document.getElementById("saving_pie_chart");
                var myChart = new Chart(ctx, {
                    type: "doughnut",
                    data: {
                      labels: ["Cooling", "Baseload", "Heating"],
                      datasets: [
                      {
                          label: "Utility Cost Savings ('''+ self.currency_str +''')",
                          backgroundColor: ["rgba(31,78,121,1)", "rgba(127,127,127,1)", "rgba(192,0,0,1)"],
                          data: ['''+str(self.building.cooling_old_cost - self.building.cooling_new_cost)+''',
                                 '''+str(self.building.base_old_cost - self.building.base_new_cost)+''',
                                 '''+str(self.building.heating_old_cost - self.building.heating_new_cost)+''']
                      }
                      ]
                  },
                  options: {
                      legend: {
                         position: "bottom"
                          },

                    tooltips: {
                      callbacks: {
                        label: function(tooltipItem, data) {
                            var dataset = data.datasets[tooltipItem.datasetIndex];
                            var meta = dataset._meta[Object.keys(dataset._meta)[0]];
                            var total = meta.total;
                            var currentValue = Math.round(data.datasets[0].data[tooltipItem.index]).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")+' '''+ self.currency_str +'''';
                            var percentage = parseFloat((dataset.data[tooltipItem.index]/total*100).toFixed(1));
                            return currentValue + ' (' + percentage + '%)';
                        },
                    },
                    responsive: true,
                    enabled: true
                },

            }
            });
            </script>
        '''

        # print(self.saving_pie_str)


    @staticmethod
    def add_3d_scatter_trace(name, v_x, v_y, v_z, info, v_s, c_str):
        import math

        # Sanitize data
        v_x = ['null' if isinstance(x, str) else x for x in v_x]
        v_y = ['null' if isinstance(x, str) else x for x in v_y]
        v_z = ['null' if isinstance(x, str) else x for x in v_z]
        v_s = ['null' if isinstance(x, str) else x for x in v_s]

        trace_str = ''
        trace_str = '''
            {{
                "name": "Building in {}",
                "type": "scatter3d",
                "x": {},
                "y": {},
                "z": {},
                "mode": "markers",
                "text": "{}",
                "marker": {{
                    "autocolorscale": true,
                    "sizeref": 0.8,
                    "size": {},
                    "color": "{}",
                    "line": {{
                        "color": "rgba(186, 63, 63, 0.9)",
                        "width": 0.5
                    }},
                    "opacity": 0.9
                }}
            }}
        '''.format(name, list(v_x), list(v_y), list(v_z), info, list(v_s), c_str)
        trace_str += ','
        return (trace_str)


    @staticmethod
    def add_2d_scatter_trace(name, v_x, v_y, v_info, v_s, c_str):
        import math

        # Sanitize data
        v_x = ['null' if isinstance(x, str) else x for x in v_x]
        v_y = ['null' if isinstance(x, str) else x for x in v_y]
        v_s = ['null' if isinstance(x, str) else x for x in v_s]

        trace_str = ''
        trace_str = '''
            {{
                "type": "scatter",
                "name": "{}",
                "x": {},
                "y": {},
                "mode": "markers",
                "text": "{}",
                "hoverinfo" : "text",
                "marker": {{
                    "autocolorscale": true,
                    "sizeref": 0.8,
                    "size": {},
                    "color": "{}",
                    "line": {{
                        "width": 2
                    }},
                    "opacity": 0.9
                }}
            }}
        '''.format(name, list(v_x), list(v_y), v_info, list(v_s), c_str)
        trace_str += ','
        return (trace_str)


    @staticmethod
    def add_2d_scatter_plot(df_summary):
        div_id_1 = 'cost_saving_bubble_plot'
        div_id_2 = 'pct_saving_bubble_plot'
        v_building_ids = df_summary['Building ID']
        cost_scatter_html = ''
        cost_scatter_html += '''
            <div id="'''+div_id_1+'''" style="height: 100%; width: 100%;" class="plotly-graph-div"></div>
            <script type="text/javascript">
            window.PLOTLYENV = window.PLOTLYENV || {};
            window.PLOTLYENV.BASE_URL = "https://plot.ly";
            Plotly.newPlot("'''+div_id_1+'''", ['''

        pct_scatter_html = ''
        pct_scatter_html += '''
            <div id="'''+div_id_2+'''" style="height: 100%; width: 100%;" class="plotly-graph-div"></div>
            <script type="text/javascript">
            window.PLOTLYENV = window.PLOTLYENV || {};
            window.PLOTLYENV.BASE_URL = "https://plot.ly";
            Plotly.newPlot("'''+div_id_2+'''", ['''

        v_rgb_str = np.random.choice(constants.Constants.rgb_color_strs, replace=False)

        # Re-scale the bubble sizes.
        v_cost_savings = df_summary['Building Annual Energy Cost Savings ($)'] # Bubble size by absolute cost savings ($)
        v_pct_savings = df_summary['Building Annual Energy Saving (%)'] # Bubble size by energy saving percentages (%)

        delta_1 = max(max(v_cost_savings) - min(v_cost_savings),1)
        delta_2 = max(max(v_pct_savings) - min(v_pct_savings),1)

        df_summary['Bubble Size 1'] = [round(((x - min(v_cost_savings)) + 0.5*delta_1)/delta_1*15, 1) * 1.5  for x in v_cost_savings]
        df_summary['Bubble Size 2'] = [round(((x - min(v_pct_savings)) + 0.5*delta_2)/delta_2*15, 1) * 1.5  for x in v_pct_savings]

        for i, building_id in enumerate(v_building_ids):
            df_temp = df_summary.loc[df_summary['Building ID']==building_id]
            location = df_temp.iloc[0]['Building Address']

            v_x = df_temp['Building Annual Electricity EUI (kWh/m2)']
            v_y = df_temp['Building Annual Fossil Fuel EUI (kWh/m2)']
            v_s_1 = df_temp['Bubble Size 1']
            v_s_2 = df_temp['Bubble Size 2']

            v_info = 'Building ID: ' + str(df_temp['Building ID'][i]) + ' <br>'
            v_info += 'Building Location: ' + str(df_temp['Building Address'][i]) + ' <br>'
            v_info += 'Annual electricity EUI : ' + str(df_temp['Building Annual Electricity EUI (kWh/m2)'][i]) + ' (kWh/m<sup>2</sup>) <br>'
            v_info += 'Annual fossil fuel EUI : ' + str(df_temp['Building Annual Fossil Fuel EUI (kWh/m2)'][i]) + ' (kWh/m<sup>2</sup>) <br>'
            v_info += 'Potential cost savings: $' + '{:,}'.format(df_temp['Building Annual Energy Cost Savings ($)'][i]) + ' <br>'
            v_info += 'Potential energy savings: ' + str(df_temp['Building Annual Energy Saving (%)'][i]) + '%'

            c_str_1 = 'rgb(0, 51, 102)'
            c_str_2 = 'rgb(0, 51, 102)'

            cost_scatter_html +=  '\n' + Report.add_2d_scatter_trace(location, v_x, v_y, v_info, v_s_1, c_str_1)
            pct_scatter_html +=  '\n' + Report.add_2d_scatter_trace(location, v_x, v_y, v_info, v_s_2, c_str_2)

        cost_scatter_html += '''
            ],
            {
              "title": "Building Saving Opportunities",
              "hovermode": "closest",
              "height": 1000,
              "xaxis": { "title": "Building Annual Electricity EUI (kWh/m2)", "ticklen": 5, "gridwidth": 2 },
              "yaxis": { "title": "Building Annual Fossil Fuel EUI (kWh/m2)", "ticklen": 5, "gridwidth": 2 },
              "legend": { "x": 0, "y": 1, "orientation": "h" },
              "showlegend": false
            },
            {
              "showLink": true,
              "linkText": "Export to plot.ly"
            }
            )

            </script>
            <script type="text/javascript">
            window.addEventListener("resize", function() { Plotly.Plots.resize(document.getElementById("''' + div_id_1 + '''")); });
            </script>
        '''

        pct_scatter_html += '''
            ],
            {
              "title": "Building Saving Opportunities",
              "hovermode": "closest",
              "height": 1000,
              "xaxis": { "title": "Building Annual Electricity EUI (kWh/m2)", "ticklen": 5, "gridwidth": 2 },
              "yaxis": { "title": "Building Annual Fossil Fuel EUI (kWh/m2)", "ticklen": 5, "gridwidth": 2 },
              "legend": { "x": 0, "y": 1, "orientation": "h" },
              "showlegend": false
            },
            {
              "showLink": true,
              "linkText": "Export to plot.ly"
            }
            )

            </script>
            <script type="text/javascript">
            window.addEventListener("resize", function() { Plotly.Plots.resize(document.getElementById("''' + div_id_2 + '''")); });
            </script>
        '''

        return (cost_scatter_html, pct_scatter_html)


    def generate_portfolio_report(self, report_path):
        report_file = os.path.join(
            report_path,
            str(self.portfolio.name) + '_report.html'
        )
        with open(report_file, 'w', encoding="utf-8") as report_html:
            report_html.write('<!DOCTYPE html>')
            report_html.write('<html>')
            report_html.write('<title>Building Efficiency Targeting Tool for Energy Retrofits (BETTER) Report</title>')
            report_html.write(self.html_basic())

            report_html.write('<body class="w3-light-grey w3-content" style="max-width:1500px">')

            # Navigation bar
            report_html.write(self.navigation_bar())

            # Portfolio overview card
            report_html.write('''
            <div class="w3-container w3-padding-large w3-white"> <h2 id="overview"><b>Portfolio Summary</b></h2>
                <hr class="w3-opacity">
                <div class="w3-container w3-margin-bottom w3-padding-small">
                    <table class="w3-table w3-bordered w3-border">
                        <tr>
                            <td width="50%" class="td_border" colspan="3"><b>Portfolio Name</b></td>
                            <td width="50%" class="td_border" colspan="3">''' + self.portfolio.name + '''</td>
                        </tr>
                        <tr>
                            <td width="50%" class="td_border" colspan="3"><b>Number of Buildings</b></td>
                            <td width="50%" class="td_border" colspan="3">''' + '{:,}'.format(self.portfolio.n_buildings) + '''</td>
                        </tr>
                        <tr>
                            <td width="50%" class="td_border" colspan="3"><b>Total Building Area (m<sup>2</sup>)</b></td>
                            <td width="50%" class="td_border" colspan="3">''' + '{:,}'.format(int(self.portfolio.total_area)) + '''</td>
                        </tr>
                    </table> <br>
                    <table class="w3-table w3-bordered w3-border" style="width:95% border: solid 1 px blue">
                        <tr>
                            <td width="50%" class="td_border" colspan="4"></td>
                            <td width="25%" class="td_border" colspan="4"><b>Electricity</b></td>
                            <td width="25%" class="td_border" colspan="4"><b>Fossil Fuel</b></td>
                        </tr>
                        <tr>
                            <td width="50%" class="td_border" colspan="4"><b>Portfolio Annual Consumption (kWh)</b></td>
                            <td width="25%" class="td_border" colspan="4">''' + '{:,}'.format(self.portfolio.total_annual_consumption_e) + '''</td>
                            <td width="25%" class="td_border" colspan="4">''' + '{:,}'.format(self.portfolio.total_annual_consumption_f) + '''</td>
                        </tr>
                        <tr>
                            <td width="50%" class="td_border" colspan="4"><b>Portfolio Annual Cost ($)</b></td>
                            <td width="25%" class="td_border" colspan="4">''' + '{:,}'.format(self.portfolio.total_annual_cost_e) + '''</td>
                            <td width="25%" class="td_border" colspan="4">''' + '{:,}'.format(self.portfolio.total_annual_cost_f) + '''</td>
                        </tr>
                        <tr>
                            <td width="50%" class="td_border" colspan="4"><b>Portfolio Average Annual Site EUI (kWh/m<sup>2</sup>)</b></td>
                            <td width="25%" class="td_border" colspan="4">''' + '{:,}'.format(self.portfolio.portfolio_eui_e) + '''</td>
                            <td width="25%" class="td_border" colspan="4">''' + '{:,}'.format(self.portfolio.portfolio_eui_f) + '''</td>
                        </tr>
                    </table>
                    <p style="margin:0px;">&nbsp;&nbsp;<i>Note: The annual results are from the most recent 12 months' input.</i></p>
                </div>
            </div><br>
            ''')


            # Portfolio summary charts card
            scatter_html = self.add_2d_scatter_plot(self.portfolio.df_bldg_summary)[0]
            report_html.write('''
            <div class="w3-container w3-padding-large w3-white"> <h2 id="about"><b>Benchmarking</b></h2>
                <hr class="w3-opacity">
                <div class="w3-container w3-margin-bottom w3-col m12 w3-padding-small">
                    <div class="w3-container ">

                        ''' + 
                            ''' The chart below shows the energy use intensities and savings potentials of each building in your portfolio. 
                            The X-axis represents annual electricity use intensity, and the Y-axis represents annual fossil fuel energy use intensity. 
                            If your building is all-electric, it will sit somewhere at the bottom of the chart, since fossil fuel EUI will be zero. 
                            Bubble size indicates the potential utility cost savings in US dollars – the bigger the bubble, the higher that building’s savings potential.
                            
                            Hover your cursor over each bubble to display key stats about each building, including its ID from the Portfolio input spreadsheet, its location, 
                            its annual electricity and fossil fuel EUI, its potential cost savings, and its potential energy savings percentage. '''
                        + '''<br>

                        ''' + scatter_html + '''
                    </div>
                </div>
                <div class="w3-container w3-margin-bottom w3-padding-small"></div>
            </div><br>
            ''')

            # # Bubble chart size-by-pct, hidden by default
            # report_html.write('<div class="w3-cell-row" id="bubble_plot" style = "display:none">')
            # #report_html.write('<div class="w3-container w3-cell w3-mobile">')
            # report_html.write('''
            #     <div id="bubble_plot" class = "w3-row-padding">
            #         <canvas id="pct_saving_bubble_plot"></canvas>
            #     </div>''')
            # scatter_html = self.add_2d_scatter_plot(self.portfolio.df_bldg_summary)[1]
            # report_html.write('''
            # <div class="w3-container w3-padding-large w3-white"> <h2 id="about"><b>Benchmarking</b></h2>
            #     <hr class="w3-opacity">
            #     <div class="w3-container w3-margin-bottom w3-col m12 w3-padding-small">
            #         <div class="w3-container ">

            #             ''' + 
            #                 ''' The chart below shows the energy use intensities and savings potentials of each building in your portfolio. 
            #                 The X-axis represents annual electricity use intensity, and the Y-axis represents annual fossil fuel energy use intensity. 
            #                 If your building is all-electric, it will sit somewhere at the bottom of the chart, since fossil fuel EUI will be zero. 
            #                 Bubble size indicates the potential utility cost savings in US dollars – the bigger the bubble, the higher that building’s savings potential.
                            
            #                 Hover your cursor over each bubble to display key stats about each building, including its ID from the Portfolio input spreadsheet, its location, 
            #                 its annual electricity and fossil fuel EUI, its potential cost savings, and its potential energy savings percentage. '''
            #             + '''<br>

            #             ''' + scatter_html + '''
            #         </div>
            #     </div>
            #     <div class="w3-container w3-margin-bottom w3-padding-small"></div>
            # </div><br>
            # ''')

            # Building details table card
            tbstr = ''
            tbstr += '<table border="1" class="dataframe w3-table w3-bordered w3-border tablesorter" id="myTable"">\n'
            tbstr += '    <thead>\n'
            tbstr += '      <tr style=" text-align: right;">\n'
            for col_name in self.portfolio.df_bldg_summary.columns:
                if col_name != 'Detail Report' and not col_name.startswith('Bubble Size'): 
                    tbstr += '          <th>' + col_name + '</th>\n'
            tbstr += '      </tr>\n'
            tbstr += '    </thead>\n'
            tbstr += '    <tbody>\n'
            for n in range(0, len(self.portfolio.df_bldg_summary.axes[0])):
                tbstr += '        <tr>\n'
                tbstr += '            <td><a href=' + report_path + str(self.portfolio.df_bldg_summary['Detail Report'][n]) + '>' + str(self.portfolio.df_bldg_summary['Building ID'][n]) + '</a></td>\n'
                tbstr += '            <td>' + self.portfolio.df_bldg_summary['Building Name'][n] + '</td>\n'
                tbstr += '            <td>' + self.portfolio.df_bldg_summary['Building Address'][n] + '</td>\n'
                tbstr += '            <td>' + self.format_number(self.portfolio.df_bldg_summary['Building Area (m2)'][n]) + '</td>\n'
                tbstr += '            <td>' + self.format_number(self.portfolio.df_bldg_summary['Building Annual Electricity Consumption (kWh)'][n]) + '</td>\n'
                tbstr += '            <td>' + self.format_number(self.portfolio.df_bldg_summary['Building Annual Fossil Fuel Consumption (kWh)'][n]) + '</td>\n'
                tbstr += '            <td>' + self.format_number(self.portfolio.df_bldg_summary['Building Annual Electricity Cost ($)'][n]) + '</td>\n'
                tbstr += '            <td>' + self.format_number(self.portfolio.df_bldg_summary['Building Annual Fossil Fuel Cost ($)'][n]) + '</td>\n'
                tbstr += '            <td>' + self.format_number(self.portfolio.df_bldg_summary['Building Annual Electricity EUI (kWh/m2)'][n]) + '</td>\n'
                tbstr += '            <td>' + self.format_number(self.portfolio.df_bldg_summary['Building Annual Fossil Fuel EUI (kWh/m2)'][n]) + '</td>\n'
                tbstr += '            <td>' + self.format_number(self.portfolio.df_bldg_summary['Building Annual Energy Cost Savings ($)'][n]) + '</td>\n'
                tbstr += '            <td>' + self.format_number(self.portfolio.df_bldg_summary['Building Annual Energy Saving (%)'][n]) + '</td>\n'
                tbstr += '        </tr>\n'
            tbstr += '    </tbody>\n'
            tbstr += '</table>\n'
            report_html.write('''
            <div class="w3-container w3-padding-large w3-white"> <h2 id="about"><b>Building Details</b></h2>
                <hr class="w3-opacity">
                <div class="w3-container w3-margin-bottom w3-col m12 w3-padding-small">
                    <div class="w3-container ">
                        
                        ''' + 
                            ''' The table below lists key building information for all buildings in your portfolio, including energy consumption, 
                            energy cost, and saving potentials. Click on the table headers to sort the buildings according to that metric (for example, 
                            clicking on “Building Annual Energy Cost Savings” will sort the buildings from lowest to highest cost savings potential, 
                            and clicking again will sort from highest to lowest).
                            For detailed analysis results of a single building, click on the link in the “Building ID” column for that building. '''
                        + ''' <br>
                        ''' + tbstr + '''
                    </div>
                </div>
                <div class="w3-container w3-margin-bottom w3-padding-small"></div>
            </div><br>
            ''')

            # Footer card
            report_html.write('  <!-- Footer -->')
            report_html.write('  <footer class="w3-container w3-padding-32 w3-white">')
            report_html.write('  <div class="w3-row-padding">')
            report_html.write('    <div class="w3-half">')
            report_html.write('      <h3>Partners</h3>')
            # report_html.write('      <p>Place holder.</p>')
            report_html.write(self.equans_logo)
            report_html.write(self.icf_logo)
            report_html.write(self.jci_logo)
            report_html.write('    </div>')
            report_html.write('    <div class="w3-half">')
            report_html.write('      <h3>Links</h3>')
            report_html.write('      <ul class="w3-ul w3-hoverable">')
            report_html.write('        <li class="w3-padding-16">')
            report_html.write('          <span class="w3-large"><a href="https://github.com/LBNL-CERC-BEE/CERC-BEE-Virtual-Energy-Efficiency-Targeting-Tool">GitHub Repository</a></span><br>')
            report_html.write('        </li>')
            report_html.write('      </ul>')
            report_html.write('    </div>')
            report_html.write('  </div>')
            report_html.write('  </footer>')
            report_html.write('  <div class="w3-black w3-center w3-padding-24"></div>')


            report_html.write('<script>')
            # Show/hide trends
            report_html.write('function showTrends() {')
            report_html.write('    var x = document.getElementById("bubble_plot");')
            report_html.write('    if (x.style.display === "none") {')
            report_html.write('        x.style.display = "block";')
            report_html.write('    } else {')
            report_html.write('        x.style.display = "none";')
            report_html.write('    }')
            report_html.write('}')
            report_html.write('</script>')

            report_html.write('</body>')

            report_html.write('''
            <script type="text/javascript">
                $(function() {
                    $("#myTable").tablesorter();
                });
            </script>
            ''')

            report_html.write('</html>')

        return