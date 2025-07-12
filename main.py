from requirements import *
from components import *
from colorama import Fore, Style, init
import os

# Initialize colorama for Windows compatibility
init(autoreset=True)

class CaniRun():
    def __init__(self):
        self.pc_components = []
        self.game_requirements = []
        
    def check(self, id, minimum=True):
        print(f"{Fore.CYAN}🎮 Checking game compatibility...{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}📊 Gathering system information...{Style.RESET_ALL}")
        try:
         self.game_requirements.append(get_requirements(id, minimum=True)) if minimum==True else self.game_requirements.append(get_requirements(id, minimum=False))
         self.pc_components.append(get_components())
        except:
         return input(Fore.RED+'STEAM GAME ID IS NOT VALID, PLEASE RESTART THE PROGRAM AND TRY AGAIN (PRESS ENTER TO EXIT)'+Fore.RESET) 
        self.compare(id=id)

    def format_value(self, value, unit=""):
        """Format values for better display"""
        if value is None:
            return "Unknown / Not Have"
        if isinstance(value, float):
            return f"{value:.1f} {unit}".strip()
        return f"{value} {unit}".strip()

    def get_status_icon(self, passed):
        """Get appropriate icon based on status"""
        return "✅" if passed else "❌"

    def get_percentage(self, your_value, required_value):
        """Calculate percentage of requirement met"""
        if your_value is None or required_value is None:
            return 0
        try:
            return min(100, (your_value / required_value) * 100)
        except (ZeroDivisionError, TypeError):
            return 0

    def print_header(self, game):
        """Print a nice header"""
        print("\n" + "="*60)
        print(f"{Fore.CYAN}{Style.BRIGHT}🎮 CAN I RUN THIS GAME? 🎮{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{Style.BRIGHT} {game} {Style.RESET_ALL}")
        print("="*60)

    def print_component_check(self, component_name, icon, your_value, required_value, unit, passed):
        """Print formatted component check result"""
        status_color = Fore.GREEN if passed else Fore.RED
        percentage = self.get_percentage(your_value, required_value)
        
        print(f"\n{icon} {Fore.CYAN}{Style.BRIGHT}{component_name}{Style.RESET_ALL}")
        print(f"   Your System: {Fore.YELLOW}{self.format_value(your_value, unit)}{Style.RESET_ALL}")
        print(f"   Required:    {Fore.MAGENTA}{self.format_value(required_value, unit)}{Style.RESET_ALL}")
        print(f"   Status:      {status_color}{Style.BRIGHT}{'PASSED' if passed else 'FAILED'}{Style.RESET_ALL}")
        
        if percentage > 0:
            print(f"   Performance: {self.get_progress_bar(percentage)} {percentage:.1f}%")

    def get_progress_bar(self, percentage):
        """Create a visual progress bar"""
        bar_length = 20
        filled_length = int(bar_length * percentage / 100)
        
        if percentage >= 100:
            color = Fore.GREEN
        elif percentage >= 70:
            color = Fore.YELLOW
        else:
            color = Fore.RED
            
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        return f"{color}[{bar}]{Style.RESET_ALL}"

    def get_overall_status(self, results):
        """Determine overall compatibility status"""
        passed_count = sum(1 for result in results if result['passed'])
        total_count = len(results)
        
        if passed_count == total_count:
            return "🎉 FULLY COMPATIBLE", Fore.GREEN
        elif passed_count >= total_count * 0.75:
            return "⚠️ MOSTLY COMPATIBLE", Fore.YELLOW
        elif passed_count >= total_count * 0.5:
            return "🔧 PARTIALLY COMPATIBLE", Fore.YELLOW
        else:
            return "❌ NOT COMPATIBLE", Fore.RED

    def print_summary(self, results):
        """Print final summary"""
        status, color = self.get_overall_status(results)
        passed_count = sum(1 for result in results if result['passed'])
        total_count = len(results)
        
        print("\n" + "="*60)
        print(f"{color}{Style.BRIGHT}{status}{Style.RESET_ALL}")
        print(f"Components Passed: {Fore.CYAN}{passed_count}/{total_count}{Style.RESET_ALL}")
        print("="*60)
        
        # Provide recommendations
        failed_components = [r for r in results if not r['passed']]
        if failed_components:
            print(f"\n{Fore.RED}⚠️ Components that need upgrading:{Style.RESET_ALL}")
            for comp in failed_components:
                print(f"   • {comp['name']}")
                
        if passed_count == total_count:
            print(f"\n{Fore.GREEN}🎮 You're all set to play this game!{Style.RESET_ALL}")
        elif passed_count >= total_count * 0.75:
            print(f"\n{Fore.YELLOW}🎮 Game should run, but consider upgrading failed components for better performance.{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}🎮 Game may not run properly. Consider upgrading the failed components.{Style.RESET_ALL}")

    def compare(self,id):
        """Enhanced comparison function with better UX/UI"""
        game_name = get_game_name(id=id)
        self.print_header(game=game_name)
        
        # Get component values
        pc_size, pc_cpu_freq, pc_cpu_cores, pc_gpu_memory, pc_ram = self.pc_components[0]
        req_size, req_cpu_freq,req_cpu_cores, req_gpu_memory, req_ram = self.game_requirements[0]
        
        # Check each component
        results = []
        
        # Storage check
        size_passed = pc_size >= req_size if req_size else True
        results.append({'name': 'Storage Space', 'passed': size_passed})
        self.print_component_check(
            "💾 Storage Space",
            self.get_status_icon(size_passed),
            pc_size, req_size, "GB",
            size_passed
        )
        
        # CPU check
        cpu_passed = pc_cpu_freq >= req_cpu_freq if req_cpu_freq and req_cpu_freq != 'None' else True
        results.append({'name': 'CPU Frequency', 'passed': cpu_passed})
        self.print_component_check(
            "🖥️ CPU Frequency",
            self.get_status_icon(cpu_passed),
            pc_cpu_freq, req_cpu_freq, "MHz",
            cpu_passed
        )
        # CPU cores check
        cpu_core_passed = pc_cpu_cores >= req_cpu_cores if req_cpu_cores and req_cpu_cores != 'None' else True
        results.append({'name': 'CPU Cores', 'passed': cpu_core_passed})
        self.print_component_check(
            "🖥️ CPU Cores",
            self.get_status_icon(cpu_core_passed),
            pc_cpu_cores, req_cpu_cores, "Core/s",
            cpu_core_passed
        )
        
        # GPU check
        gpu_passed = False
        if pc_gpu_memory and req_gpu_memory:
            gpu_passed = pc_gpu_memory >= req_gpu_memory
        elif not req_gpu_memory:
            gpu_passed = True
            
        results.append({'name': 'GPU Memory', 'passed': gpu_passed})
        self.print_component_check(
            "🎮 GPU Memory",
            self.get_status_icon(gpu_passed),
            pc_gpu_memory, req_gpu_memory, "GB",
            gpu_passed
        )
        
        # RAM check
        ram_passed = False
        if(req_ram == None): ram_passed = False
        else:
         if(req_ram >= req_ram or (req_ram - req_ram) < 0.3 ): ram_passed= True
        results.append({'name': 'RAM Memory', 'passed': ram_passed})
        self.print_component_check(
            "🧠 RAM Memory",
            self.get_status_icon(ram_passed),
            pc_ram, req_ram, "GB",
            ram_passed
        )
        
        # Print final summary
        self.print_summary(results)
        
        # Additional tips
        print(f"\n{Fore.CYAN}💡 Tips:{Style.RESET_ALL}")
        print("   • Close unnecessary programs before gaming")
        print("   • Update your graphics drivers")
        print("   • Consider lowering game settings if performance is poor")
        print("   • Check for game-specific optimization guides")

if __name__ == '__main__':
    id = input(f"Enter the game steam id (like: 'https://store.steampowered.com/app/{Fore.RED}271590{Fore.RESET}/'):")
    if id.isdigit():
     requirements = int(input('Type 1 for minimum requirements or 2 for recommended requirements:'))
     run = CaniRun()
     run.check(id, minimum=True) if requirements == 1 else run.check(id,minimum=False)
    else:
        input(Fore.RED+ 'THE ID MUST BE A INTEGER! PRESS ENTER TO EXIT')
        exit()