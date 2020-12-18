project "libpqxx"
	kind "SharedLib"
	language "C++"
	cppdialect "C++17"

	targetdir ("%{wks.location}/bin/" .. outputdir .. "/stockmon")
	objdir ("bin-int/" .. outputdir .. "/%{prj.name}")

	defines
	{
		"PQXX_SHARED",
		"pqxx_EXPORTS"
	}

	files
	{
		"include/pqxx/*",
    	"src/*"
	}

	links
	{
		"%{wks.location}/vendor/libpq/win/lib/libpq.lib",
		"wsock32.lib",
		"ws2_32.lib",
		"gdi32.lib",
		"advapi32.lib"
	}

	includedirs
	{
		"%{wks.location}/vendor/libpqxx/include",
		"%{wks.location}/vendor/libpqxx/config/include",
		"%{wks.location}/vendor/libpq/include"
	}

	filter "configurations:Debug"
		runtime "Debug"
		symbols "on"

	filter "configurations:Release"
		runtime "Release"
		optimize "on"
