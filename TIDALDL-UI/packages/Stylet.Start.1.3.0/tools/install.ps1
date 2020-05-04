param($installPath, $toolsPath, $package, $project)

# Testing: call with Invoke-Expression "path\to\install.ps1"
$project = Get-Project

$rootNamespace = $project.Properties.Item("RootNamespace").Value
$rootPath = $project.Properties.Item("LocalPath").Value

# VS writes its files as UTF-8 with a BOM. We should do the same.
$encoding = New-Object System.Text.UTF8Encoding($true);

# Modify App.xaml
# This is a real ballache: the previous Stylet.Start package (which uses NuGet's 'content' approach)
# will delete App.xaml and App.xaml.cs on uninstallation if they haven't been modified by the user.
# Obviously that's bad, so we'll need to put them back

$appXamlPath = [System.IO.Path]::Combine($rootPath, "App.xaml")
$existingAppXaml = $project.ProjectItems | Where { $_.Name -eq "App.xaml" } | Select -First 1
if ($existingAppXaml -eq $null)
{
    Write-Host ">>>> App.xaml is missing: creating it from scratch (it was probably removed by NuGet)"

    $appXamlContent = "<Application x:Class=""${rootNamespace}.App""
             xmlns=""http://schemas.microsoft.com/winfx/2006/xaml/presentation""
             xmlns:x=""http://schemas.microsoft.com/winfx/2006/xaml""
             xmlns:s=""https://github.com/canton7/Stylet""
             xmlns:local=""clr-namespace:${rootNamespace}"">
    <Application.Resources>
       <s:ApplicationLoader>
            <s:ApplicationLoader.Bootstrapper>
                <local:Bootstrapper/>
            </s:ApplicationLoader.Bootstrapper>
        </s:ApplicationLoader>
    </Application.Resources>
</Application>"

    [System.IO.File]::WriteAllText($appXamlPath, $appXamlContent, $encoding)
    $appXaml = $project.ProjectItems.AddFromFile($appXamlPath)
    $appXaml.Properties.Item("BuildAction").Value = 4 # ApplicationDefinition
}
else
{
    $doc = [System.Xml.Linq.XDocument]::Load($appXamlPath)

    $styletNs = [System.Xml.Linq.XNamespace]::Get("https://github.com/canton7/Stylet")
    $ns = $doc.Root.GetDefaultNamespace()
    $localNs = $doc.Root.GetNamespaceOfPrefix("local")

    $startupUri = $doc.Root.Attribute("StartupUri")
    if ($startupUri -ne $null)
    {
        $startupUri.Remove()
    }

    $existingApplicationLoader = $doc.Root.Descendants($styletNs.GetName("ApplicationLoader")) | Select -First 1
    if ($existingApplicationLoader -ne $null)
    {
        Write-Host ">>>> Not modifying App.xaml as it already has an <s:ApplicationLoader> element"
    }
    else
    {
        if ($doc.Root.Attribute([System.Xml.Linq.XNamespace]::Xmlns.GetName("s")) -eq $null)
        {
            $doc.Root.Add((New-Object System.Xml.Linq.XAttribute([System.Xml.Linq.XNamespace]::Xmlns.GetName("s"), $styletNs)))
        }

        $resources = $doc.Root.Element($ns.GetName("Application.Resources"))
        $existingResources = @($resources.Nodes())

        $bootstrapper = New-Object System.Xml.Linq.XElement($localNs.GetName("Bootstrapper"))
        $bootstrapperProperty = New-Object System.Xml.Linq.XElement($styletNs.GetName("ApplicationLoader.Bootstrapper"), $bootstrapper)
        $applicationLoader = New-Object System.Xml.Linq.XElement($styletNs.GetName("ApplicationLoader"), $bootstrapperProperty)

        if ($existingResources.Count -gt 0)
        {
            $mergedDictionaries = New-Object System.Xml.Linq.XElement($ns.GetName("ResourceDictionary.MergedDictionaries"), $applicationLoader)
            $resourceDictionary = New-Object System.Xml.Linq.XElement($ns.GetName("ResourceDictionary"), $mergedDictionaries, $existingResources)
            $resources.ReplaceNodes($resourceDictionary)
        }
        else
        {
            $resources.Add($applicationLoader)
        }

        $settings = New-Object System.Xml.XmlWriterSettings
        $settings.Indent = $True
        $settings.NewLineOnAttributes = $True
        $settings.OmitXmlDeclaration = $True
        $settings.IndentChars = "    "

        $stringWriter = New-Object System.IO.StringWriter
        $xmlWriter = [System.Xml.XmlWriter]::Create($stringWriter, $settings)
        $doc.WriteTo($xmlWriter)
        $xmlWriter.Close()

        $appXaml = $stringWriter.ToString();
        $stringWriter.Close()

        # Manually fudge the newlines after xmlns declarations, since XmlWriter won't do them itself
        $appXaml = [System.Text.RegularExpressions.Regex]::Replace($appXaml, "Application\s+x:Class=", "Application x:Class=")
        $appXaml = $appXaml.Replace(" xmlns=", "`r`n             xmlns=")
        $appXaml = $appXaml.Replace(" xmlns:", "`r`n             xmlns:")

        [System.IO.File]::WriteAllText($appXamlPath, $appXaml, $encoding)
    }
}

# Add bootstrapper

# Only do this if Bootstrapper.cs doesn't already exist...
$existingBootstrapper = $project.ProjectItems | Where { $_.Name -eq "Bootstrapper.cs" } | Select -First 1
if ($existingBootstrapper -ne $null)
{
    Write-Host ">>>> Not creating Bootstrapper.cs as it already exists"
}
else
{
    $bootstrapperContent = "using System;
using Stylet;
using StyletIoC;
using ${rootNamespace}.Pages;

namespace ${rootNamespace}
{
    public class Bootstrapper : Bootstrapper<ShellViewModel>
    {
        protected override void ConfigureIoC(IStyletIoCBuilder builder)
        {
            // Configure the IoC container in here
        }

        protected override void Configure()
        {
            // Perform any other configuration before the application starts
        }
    }
}
"
    $bootstrapperPath = [System.IO.Path]::Combine($rootPath, "Bootstrapper.cs")
    [System.IO.File]::WriteAllText($bootstrapperPath, $bootstrapperContent, $encoding)
    $null = $project.ProjectItems.AddFromFile($bootstrapperPath)
}

# Add Pages/ folder

$pages = $project.ProjectItems | Where { $_.Name -Eq "Pages" } | Select -First 1
if ($pages -eq $null)
{
    # This also creates the folder on disk
    $pages = $project.ProjectItems.AddFolder("Pages")
}

# Add Pages/ShellView.xaml

# Used in multiple places, potentially
$standaloneShellViewContent = "<Window x:Class=""${rootNamespace}.Pages.ShellView""
        xmlns=""http://schemas.microsoft.com/winfx/2006/xaml/presentation""
        xmlns:x=""http://schemas.microsoft.com/winfx/2006/xaml""
        xmlns:d=""http://schemas.microsoft.com/expression/blend/2008""
        xmlns:mc=""http://schemas.openxmlformats.org/markup-compatibility/2006""
        xmlns:local=""clr-namespace:${rootNamespace}.Pages""
        xmlns:s=""https://github.com/canton7/Stylet""
        mc:Ignorable=""d""
        d:DataContext=""{d:DesignInstance local:ShellViewModel}""
        Title=""Stylet Start Project""
        Width=""350"" Height=""200"">
    <TextBlock FontSize=""30"" HorizontalAlignment=""Center"" VerticalAlignment=""Center"">
        Hello Stylet!
    </TextBlock>
</Window>"

$standaloneShellViewCsContent = "using System;
using System.Windows;

namespace ${rootNamespace}.Pages
{
    /// <summary>
    /// Interaction logic for ShellView.xaml
    /// </summary>
    public partial class ShellView : Window
    {
        public ShellView()
        {
            InitializeComponent();
        }
    }
}
"

# Only do this if ShellView doesn't already exist...
$existingShellView = $pages.ProjectItems | Where { $_.Name -eq "ShellView.xaml" } | Select -First 1
if ($existingShellView -ne $null)
{
    Write-Host ">>>> Not creating Pages/ShellView.xaml as it already exists. "
}
else
{
    $mainWindow = ($project.ProjectItems | Where { $_.Name -Eq "MainWindow.xaml" } | Select -First 1)
    if ($mainWindow -eq $null)
    {
        Write-Host ">>>> Creating Pages/ShellView.xaml from scratch, as MainWindow.xaml doesn't exist"

        $shellViewContent = $standaloneShellViewContent
        $shellViewCsContent = $standaloneShellViewCsContent
    }
    else
    {
        $mainWindowPath = $mainWindow.Properties.Item("FullPath").Value
        $mainWindowCsPath = $mainWindowPath + ".cs"

        $shellViewContent = [System.IO.File]::ReadAllText($mainWindowPath)
        $match = [System.Text.RegularExpressions.Regex]::Match($shellViewContent, "<Window (.*?)>", [System.Text.RegularExpressions.RegexOptions]::Singleline)
        if ($match.Success)
        {
            $mainWindow.Remove()

            $originalShellViewAttributes = $match.Groups[1].Value
            $shellViewAttributes = $originalShellViewAttributes

            $shellViewAttributes = $shellViewAttributes.Replace("x:Class=""${rootNamespace}.MainWindow""", "x:Class=""${rootNamespace}.Pages.ShellView""")
            $shellViewAttributes = $shellViewAttributes.Replace('Title="MainWindow"', 'Title="Stylet Start Project"')
            if (!$shellViewAttributes.Contains("xmlns:local"))
            {
                $shellViewAttributes += "`r`n        xmlns:local=""clr-namespace:${rootNamespace}.Pages"""
            }
            else
            {
                $shellViewAttributes = $shellViewAttributes.Replace("xmlns:local=""clr-namespace:${rootNamespace}""", "xmlns:local=""clr-namespace:${rootNamespace}.Pages""")
            }
            if (!$shellViewAttributes.Contains("https://github.com/canton7/Stylet"))
            {
                $shellViewAttributes += "`r`n        xmlns:s=""https://github.com/canton7/Stylet"""
            }
            if (!$shellViewAttributes.Contains('mc:Ignorable="d"'))
            {
                $shellViewAttributes += "`r`n        mc:Ignorable=""d"""
            }
            if (!$shellViewAttributes.Contains("d:DataContext="))
            {
                $shellViewAttributes += "`r`n        d:DataContext=""{d:DesignInstance local:ShellViewModel}"""
            }

            $shellViewContent = $shellViewContent.Replace($originalShellViewAttributes, $shellViewAttributes);

            $shellViewContent = [System.Text.RegularExpressions.Regex]::Replace($shellViewContent, "<Grid>\s*</Grid>", "<TextBlock FontSize=""30"" HorizontalAlignment=""Center"" VerticalAlignment=""Center"">
        Hello Stylet!
    </TextBlock>")

            [System.IO.File]::Delete($mainWindowPath)

            if ([System.IO.File]::Exists($mainWindowCsPath))
            {
                $shellViewCsContent = [System.IO.File]::ReadAllText($mainWindowCsPath)
                $shellViewCsContent = $shellViewCsContent.Replace("namespace " + $rootNamespace, "namespace " + $rootNamespace + ".Pages")
                $shellViewCsContent = $shellViewCsContent.Replace("class MainWindow", "class ShellView")
                $shellViewCsContent = $shellViewCsContent.Replace("public MainWindow()", "public ShellView()")
                $shellViewCsContent = $shellViewCsContent.Replace("/// Interaction logic for MainWindow.xaml", "/// Interaction logic for ShellView.xaml")

                [System.IO.File]::Delete($mainWindowCsPath)
            }
            else
            {
                Write-Host ">>>> MainWindow.xaml.cs doesn't exist. Creating Pages/ShellView.xaml.cs from scratch"
                $shellViewCsContent = $standaloneShellViewCsContent
            }

        }
        else
        {
            Write-Host ">>>> WARNING: MainWindow.xaml is not a Window, so creating Pages/ShellView.xaml from scratch"

            $shellViewContent = $standaloneShellViewContent
            $shellViewCsContent = $standaloneShellViewCsContent
        }
    }

    $shellViewPath = [System.IO.Path]::Combine($rootPath, "Pages", "ShellView.xaml")
    $shellViewCsPath = $shellViewPath + ".cs"

    [System.IO.File]::WriteAllText($shellViewPath, $shellViewContent, $encoding)
    [System.IO.File]::WriteAllText($shellViewCsPath, $shellViewCsContent, $encoding)

    $shellView = $pages.ProjectItems.AddFromFile($shellViewPath)
    # This should have been added automagically, but just in case...
    $null = $shellView.ProjectItems.AddFromFile($shellViewCsPath)
}

# Add Pages/ShellViewModel.cs

# Only do this if ShellViewModel doesn't already exist
$existingShellViewModel = $pages.ProjectItems | Where { $_.Name -eq "ShellViewModel.cs" } | Select -First 1
if ($existingShellViewModel -ne $null)
{
    Write-Host ">>>> Not creating Pages/ShellViewModel.cs as it already exists"
}
else
{    
    $shellViewModelContent = "using System;
using Stylet;

namespace ${rootNamespace}.Pages
{
    public class ShellViewModel : Screen
    {
    }
}
"

    $shellViewModelPath = [System.IO.Path]::Combine($rootPath, "Pages", "ShellViewModel.cs")
    [System.IO.File]::WriteAllText($shellViewModelPath, $shellViewModelContent, $encoding)
    $null = $pages.ProjectItems.AddFromFile($shellViewModelPath)
}

Write-Host !!!
Write-Host !!! Now uninstall Stylet.Start
Write-Host !!!
